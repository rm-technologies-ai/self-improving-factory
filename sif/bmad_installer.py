"""
Headless BMAD Installation Wrapper.

REQ-024: Enables unattended BMAD installation for autonomous provisioning workflows.

The upstream BMAD installer (npx bmad-method install) is interactive and requires
user prompts via @clack/prompts. This module wraps the installer with pexpect to
automate prompt responses.

Usage:
    from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

    config = BMADInstallerConfig(
        version="6.0.0-Beta.5",
        user_name="Roy",
        language="English"
    )
    result = install_bmad_headless(target_path, config)
    if result.success:
        print("BMAD installed successfully")

CLI:
    python -m sif.bmad_installer --version 6.0.0-Beta.5 --user-name Roy /path/to/project
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pexpect
except ImportError:
    pexpect = None  # Will raise error when used

logger = logging.getLogger(__name__)


class BMADInstallerError(Exception):
    """Base exception for BMAD installer errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}


@dataclass
class BMADInstallerConfig:
    """Configuration for headless BMAD installation."""

    version: str = "latest"
    user_name: str = "Developer"
    language: str = "English"
    output_dir: str = "_bmad-output"
    timeout: int = 120
    debug: bool = False
    modules: Optional[List[str]] = None
    skip_agents: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BMADInstallerConfig":
        """Create config from dictionary."""
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)


@dataclass
class BMADInstallerResult:
    """Result of BMAD installation."""

    success: bool
    exit_code: int
    mode: str = "install"  # "install", "update", "quick-update"
    response_log: List[Dict[str, str]] = field(default_factory=list)
    preserved_config: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return asdict(self)


# Prompt patterns for BMAD installer (based on @clack/prompts)
# IMPORTANT: These patterns are best-effort guesses based on expected BMAD installer behavior.
# They have not been validated against every version of the BMAD installer and may need
# adjustment if the installer's prompts change. Run integration tests against the real
# installer to validate these patterns after any BMAD version upgrade.
# Pattern matching uses regex - case-insensitive matching is applied at runtime.
BMAD_PROMPT_PATTERNS: Dict[str, Dict[str, Any]] = {
    "user_name": {
        "pattern": r"(?:What is your name|Enter your name|name\?)",
        "response_key": "user_name",
        "default": "Developer",
    },
    "language": {
        "pattern": r"(?:communication language|language preference|language\?)",
        "response_key": "language",
        "default": "English",
    },
    "output_dir": {
        "pattern": r"(?:output (?:folder|directory)|where.*output|_bmad-output)",
        "response_key": "output_dir",
        "default": "_bmad-output",
    },
    "confirm_install": {
        "pattern": r"(?:proceed|continue|confirm|install\?|y/n)",
        "response_key": None,  # Always respond with Enter/Yes
        "default": "",
    },
    "select_modules": {
        "pattern": r"(?:select.*modules|which modules|modules to install)",
        "response_key": "modules",
        "default": "",  # Accept defaults
    },
    "quick_update": {
        "pattern": r"(?:quick.?update|already installed|update existing)",
        "response_key": None,
        "default": "",  # Accept quick-update
    },
}


def detect_bmad_version(target_path: Path) -> Optional[str]:
    """
    Detect installed BMAD version in target directory.

    Checks BMAD config files for version information. BMAD stores version
    in _bmad/bmm/config.yaml or _bmad/package.json (depending on version).

    Args:
        target_path: Path to check for BMAD installation

    Returns:
        Version string if installed, None otherwise
    """
    # Primary: Check config.yaml for version info (BMAD 6.x+)
    config_yaml = target_path / "_bmad" / "bmm" / "config.yaml"
    if config_yaml.exists():
        try:
            content = config_yaml.read_text()
            # Look for bmad_version or version fields
            for pattern in [r"bmad_version:\s*([^\s\n]+)", r"^version:\s*([^\s\n]+)"]:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    return match.group(1).strip('"').strip("'")
        except IOError:
            pass

    # Fallback: Check package.json in _bmad (older BMAD versions)
    package_json = target_path / "_bmad" / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            return data.get("version")
        except (json.JSONDecodeError, IOError):
            pass

    return None


def compare_bmad_versions(version1: str, version2: str) -> int:
    """
    Compare two BMAD version strings.

    Handles versions like "6.0.0", "6.0.0-Beta.5", "latest".
    Special case: "latest" is considered greater than any version.

    Args:
        version1: First version string
        version2: Second version string

    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    # Handle special "latest" value
    if version1.lower() == "latest" and version2.lower() == "latest":
        return 0
    if version1.lower() == "latest":
        return 1
    if version2.lower() == "latest":
        return -1

    def parse_version(v: str) -> Tuple[int, ...]:
        # Handle versions like "6.0.0-Beta.5"
        v = v.lower().replace("beta", "0").replace("alpha", "-1").replace("-", ".").replace("_", ".")
        parts = re.split(r"[.\-]", v)
        result = []
        for part in parts:
            try:
                result.append(int(part))
            except ValueError:
                # Non-numeric part, skip but don't fail
                continue
        return tuple(result) if result else (0,)

    v1 = parse_version(version1)
    v2 = parse_version(version2)

    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    return 0


def _check_existing_installation(target_path: Path) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Check if BMAD is already installed and read existing config.

    Args:
        target_path: Path to check

    Returns:
        Tuple of (is_installed, existing_config_dict)
    """
    bmad_dir = target_path / "_bmad"
    if not bmad_dir.exists():
        return False, None

    config_path = bmad_dir / "bmm" / "config.yaml"
    if not config_path.exists():
        return True, None

    try:
        content = config_path.read_text()
        # Simple YAML parsing for key: value pairs
        config = {}
        for line in content.split("\n"):
            if ":" in line and not line.strip().startswith("#"):
                key, _, value = line.partition(":")
                config[key.strip()] = value.strip().strip('"').strip("'")
        return True, config
    except IOError:
        return True, None


def _build_npx_command(config: BMADInstallerConfig) -> str:
    """Build the npx command string."""
    if config.version == "latest":
        return "npx bmad-method install"
    else:
        return f"npx bmad-method@{config.version} install"


def _handle_prompt(
    child: Any,  # pexpect.spawn
    prompt_index: int,
    patterns: List[str],
    config: BMADInstallerConfig,
    response_log: List[Dict[str, str]]
) -> None:
    """
    Handle a detected prompt by sending the appropriate response.

    Args:
        child: pexpect spawn object
        prompt_index: Index of matched pattern
        patterns: List of pattern names
        config: Installation config
        response_log: Log to append responses to
    """
    # Extract the actual prompt text for logging
    before_text = ""
    if hasattr(child, "before") and child.before:
        before_text = child.before if isinstance(child.before, str) else child.before.decode("utf-8", errors="replace")

    if prompt_index >= len(patterns):
        # Unknown prompt - include actual prompt text in error for debugging
        raise BMADInstallerError(
            f"Unexpected prompt detected. Expected one of {patterns}, got index {prompt_index}. "
            f"Prompt text: {before_text[:500]}",
            details={"prompt_index": prompt_index, "before": before_text, "expected_patterns": patterns}
        )

    pattern_name = patterns[prompt_index]
    pattern_info = BMAD_PROMPT_PATTERNS.get(pattern_name, {})

    # Determine response
    response_key = pattern_info.get("response_key")
    if response_key:
        response = getattr(config, response_key, pattern_info.get("default", ""))
    else:
        response = pattern_info.get("default", "")

    # Log the response with actual prompt text for debugging
    response_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": pattern_name,
        "prompt_text": before_text[:200] if before_text else "",
        "response": response,
    })

    # Send response
    child.sendline(str(response))
    logger.debug(f"Responded to '{pattern_name}' with: {response}")


def install_bmad_headless(
    target_path: Path,
    config: Optional[BMADInstallerConfig] = None,
    preserve_existing: bool = True,
) -> BMADInstallerResult:
    """
    Install BMAD method non-interactively.

    Uses pexpect to automate the interactive installer prompts.

    Args:
        target_path: Directory to install BMAD into
        config: Installation configuration (uses defaults if not provided)
        preserve_existing: Whether to preserve existing config on reinstall

    Returns:
        BMADInstallerResult with installation status

    Raises:
        BMADInstallerError: If installation fails with unrecoverable error
    """
    if pexpect is None:
        raise BMADInstallerError(
            "pexpect is required but not installed. Run: pip install pexpect",
            details={"missing_dependency": "pexpect"}
        )

    # Validate target path exists and is a directory
    if not target_path.exists():
        raise BMADInstallerError(
            f"Target path does not exist: {target_path}",
            details={"target_path": str(target_path)}
        )
    if not target_path.is_dir():
        raise BMADInstallerError(
            f"Target path is not a directory: {target_path}",
            details={"target_path": str(target_path)}
        )

    config = config or BMADInstallerConfig()
    response_log: List[Dict[str, str]] = []
    start_time = datetime.utcnow()

    # Check existing installation
    is_installed, existing_config = _check_existing_installation(target_path)
    mode = "update" if is_installed else "install"

    if is_installed and preserve_existing:
        logger.info(f"Existing BMAD installation detected at {target_path}")

    # Build command
    cmd = _build_npx_command(config)
    logger.info(f"Running: {cmd} in {target_path}")

    # Build pattern list for pexpect
    pattern_names = list(BMAD_PROMPT_PATTERNS.keys())
    patterns = [
        BMAD_PROMPT_PATTERNS[name]["pattern"]
        for name in pattern_names
    ]

    try:
        # Spawn the process
        child = pexpect.spawn(
            cmd,
            cwd=str(target_path),
            timeout=config.timeout,
            encoding="utf-8",
        )

        if config.debug:
            child.logfile = sys.stdout

        # Main interaction loop
        while True:
            try:
                # Wait for prompt or EOF
                index = child.expect(patterns + [pexpect.EOF, pexpect.TIMEOUT])

                if index == len(patterns):  # EOF
                    break
                elif index == len(patterns) + 1:  # TIMEOUT
                    raise BMADInstallerError(
                        f"Installation timed out after {config.timeout}s",
                        details={"timeout": config.timeout}
                    )
                else:
                    # Handle the prompt
                    _handle_prompt(child, index, pattern_names, config, response_log)

            except pexpect.TIMEOUT:
                raise BMADInstallerError(
                    f"Installation timed out after {config.timeout}s",
                    details={"timeout": config.timeout, "last_output": child.before}
                )

        # Wait for process to complete
        child.close()
        exit_code = child.exitstatus or 0

        duration = (datetime.utcnow() - start_time).total_seconds()

        return BMADInstallerResult(
            success=exit_code == 0,
            exit_code=exit_code,
            mode=mode,
            response_log=response_log,
            preserved_config=existing_config if preserve_existing else None,
            duration_seconds=duration,
        )

    except FileNotFoundError as e:
        raise BMADInstallerError(
            "npx/Node.js not found. Ensure Node.js 20+ is installed.",
            details={"error": str(e)}
        )
    except pexpect.ExceptionPexpect as e:
        raise BMADInstallerError(
            f"pexpect error during installation: {e}",
            details={"error": str(e)}
        )


def parse_cli_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse CLI arguments for headless installer.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Headless BMAD Method installer wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/project
  %(prog)s --version 6.0.0-Beta.5 --user-name Roy /path/to/project
  %(prog)s --debug /path/to/project
        """,
    )

    parser.add_argument(
        "target_path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Target directory for BMAD installation (default: current directory)",
    )

    parser.add_argument(
        "--version",
        default="latest",
        help="BMAD version to install (default: latest)",
    )

    parser.add_argument(
        "--user-name",
        dest="user_name",
        default="Developer",
        help="User name for BMAD config (default: Developer)",
    )

    parser.add_argument(
        "--language",
        default="English",
        help="Communication language (default: English)",
    )

    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="_bmad-output",
        help="Output directory path (default: _bmad-output)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Installation timeout in seconds (default: 120)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output",
    )

    parser.add_argument(
        "--no-preserve",
        dest="preserve_existing",
        action="store_false",
        default=True,
        help="Do not preserve existing configuration on reinstall",
    )

    return parser.parse_args(args)


def bmad_headless_install_cli(args: Optional[List[str]] = None) -> int:
    """
    CLI entry point for headless BMAD installer.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parsed = parse_cli_args(args)

    # Set up logging
    log_level = logging.DEBUG if parsed.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Build config
    config = BMADInstallerConfig(
        version=parsed.version,
        user_name=parsed.user_name,
        language=parsed.language,
        output_dir=parsed.output_dir,
        timeout=parsed.timeout,
        debug=parsed.debug,
    )

    try:
        result = install_bmad_headless(
            target_path=parsed.target_path,
            config=config,
            preserve_existing=parsed.preserve_existing,
        )

        if result.success:
            print(f"BMAD installed successfully ({result.mode} mode)")
            print(f"Duration: {result.duration_seconds:.1f}s")
            print(f"Responses logged: {len(result.response_log)}")
            return 0
        else:
            print(f"BMAD installation failed with exit code {result.exit_code}")
            if result.error_message:
                print(f"Error: {result.error_message}")
            return result.exit_code

    except BMADInstallerError as e:
        print(f"Error: {e}")
        if parsed.debug and e.details:
            print(f"Details: {json.dumps(e.details, indent=2)}")
        return 1


if __name__ == "__main__":
    sys.exit(bmad_headless_install_cli())

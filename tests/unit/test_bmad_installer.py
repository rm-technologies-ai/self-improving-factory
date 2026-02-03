"""
Unit tests for BMAD headless installer wrapper.

TDD tests for REQ-024: Headless BMAD Installation Wrapper.

These tests define the expected behavior of the headless installer
before implementation (RED phase of TDD).
"""

import os
import sys
from pathlib import Path
from typing import Optional
from unittest.mock import Mock, patch, MagicMock

import pytest


class TestBMADInstallerImport:
    """Test that the module can be imported."""

    def test_import_bmad_installer(self):
        """Verify the bmad_installer module can be imported."""
        from sif import bmad_installer
        assert bmad_installer is not None

    def test_import_install_function(self):
        """Verify the main install function exists."""
        from sif.bmad_installer import install_bmad_headless
        assert callable(install_bmad_headless)

    def test_import_error_class(self):
        """Verify the error class exists."""
        from sif.bmad_installer import BMADInstallerError
        assert issubclass(BMADInstallerError, Exception)


class TestBMADInstallerConfig:
    """Test configuration and option handling."""

    def test_default_config_values(self):
        """Verify default configuration values are correct."""
        from sif.bmad_installer import BMADInstallerConfig

        config = BMADInstallerConfig()
        assert config.version == "latest"
        assert config.user_name == "Developer"
        assert config.language == "English"
        assert config.output_dir == "_bmad-output"
        assert config.timeout == 120

    def test_config_from_dict(self):
        """Verify config can be created from dictionary."""
        from sif.bmad_installer import BMADInstallerConfig

        config = BMADInstallerConfig.from_dict({
            "version": "6.0.0-Beta.5",
            "user_name": "Roy",
            "language": "English",
            "output_dir": "_custom-output"
        })
        assert config.version == "6.0.0-Beta.5"
        assert config.user_name == "Roy"

    def test_config_to_dict(self):
        """Verify config can be converted to dictionary."""
        from sif.bmad_installer import BMADInstallerConfig

        config = BMADInstallerConfig(user_name="Roy")
        d = config.to_dict()
        assert d["user_name"] == "Roy"
        assert "version" in d


class TestBMADInstallerPromptPatterns:
    """Test prompt detection patterns."""

    def test_prompt_patterns_defined(self):
        """Verify prompt patterns are defined."""
        from sif.bmad_installer import BMAD_PROMPT_PATTERNS

        assert isinstance(BMAD_PROMPT_PATTERNS, dict)
        assert len(BMAD_PROMPT_PATTERNS) > 0

    def test_username_prompt_pattern(self):
        """Verify username prompt pattern is defined."""
        from sif.bmad_installer import BMAD_PROMPT_PATTERNS

        assert "user_name" in BMAD_PROMPT_PATTERNS
        pattern = BMAD_PROMPT_PATTERNS["user_name"]
        assert "pattern" in pattern
        assert "response_key" in pattern

    def test_language_prompt_pattern(self):
        """Verify language prompt pattern is defined."""
        from sif.bmad_installer import BMAD_PROMPT_PATTERNS

        assert "language" in BMAD_PROMPT_PATTERNS

    def test_output_dir_prompt_pattern(self):
        """Verify output directory prompt pattern is defined."""
        from sif.bmad_installer import BMAD_PROMPT_PATTERNS

        assert "output_dir" in BMAD_PROMPT_PATTERNS


class _MockEOF(Exception):
    """Mock EOF exception for testing."""
    pass


class _MockTIMEOUT(Exception):
    """Mock TIMEOUT exception for testing."""
    pass


class _MockExceptionPexpect(Exception):
    """Mock ExceptionPexpect for testing."""
    pass


def _get_eof_index():
    """
    Get the index that represents EOF in pexpect.expect().

    The EOF index is len(BMAD_PROMPT_PATTERNS) since patterns are
    appended with [pexpect.EOF, pexpect.TIMEOUT].
    """
    from sif.bmad_installer import BMAD_PROMPT_PATTERNS
    return len(BMAD_PROMPT_PATTERNS)


class TestBMADInstallerExecution:
    """Test the main installation execution."""

    @pytest.fixture
    def mock_pexpect(self):
        """Mock pexpect for testing without actual process execution."""
        with patch("sif.bmad_installer.pexpect") as mock:
            # Set up proper exception classes
            mock.EOF = _MockEOF
            mock.TIMEOUT = _MockTIMEOUT
            mock.ExceptionPexpect = _MockExceptionPexpect
            yield mock

    def test_install_creates_command_with_version(self, mock_pexpect, tmp_path):
        """Verify the correct npx command is constructed with version."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # EOF at index len(patterns)
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig(version="6.0.0-Beta.5")
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        # Verify npx command includes version
        spawn_call = mock_pexpect.spawn.call_args
        cmd = spawn_call[0][0] if spawn_call[0] else spawn_call[1].get("command")
        assert "bmad-method@6.0.0-Beta.5" in cmd or "6.0.0-Beta.5" in str(spawn_call)

    def test_install_uses_latest_by_default(self, mock_pexpect, tmp_path):
        """Verify latest version is used by default."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # EOF at index len(patterns)
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig()  # default version = "latest"
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        spawn_call = mock_pexpect.spawn.call_args
        cmd = str(spawn_call)
        assert "bmad-method" in cmd

    def test_install_responds_to_prompts(self, mock_pexpect, tmp_path):
        """Verify prompts are handled with configured responses."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # Simulate: prompt 0 (user_name), prompt 1 (language), then EOF
        eof_idx = _get_eof_index()
        mock_child.expect.side_effect = [0, 1, eof_idx]
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig(user_name="Roy", language="English")
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        # Verify sendline was called with user responses
        assert mock_child.sendline.called

    def test_install_returns_result_object(self, mock_pexpect, tmp_path):
        """Verify installation returns a result object with status."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerResult

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # EOF immediately
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig()
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        assert isinstance(result, BMADInstallerResult)
        assert result.success is True
        assert result.exit_code == 0

    def test_install_logs_responses(self, mock_pexpect, tmp_path):
        """Verify all automated responses are logged for audit."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # Prompt 0, then EOF
        eof_idx = _get_eof_index()
        mock_child.expect.side_effect = [0, eof_idx]
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig()
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        # Result should contain log of responses
        assert hasattr(result, "response_log")
        assert isinstance(result.response_log, list)


class TestBMADInstallerErrorHandling:
    """Test error handling and compensation."""

    @pytest.fixture
    def mock_pexpect(self):
        """Mock pexpect for testing."""
        with patch("sif.bmad_installer.pexpect") as mock:
            mock.EOF = _MockEOF
            mock.TIMEOUT = _MockTIMEOUT
            mock.ExceptionPexpect = _MockExceptionPexpect
            yield mock

    def test_timeout_raises_error(self, mock_pexpect, tmp_path):
        """Verify timeout raises appropriate error."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerError

        mock_child = MagicMock()
        mock_pexpect.spawn.return_value = mock_child
        mock_child.expect.side_effect = _MockTIMEOUT("Timed out")

        config = BMADInstallerConfig(timeout=1)

        with pytest.raises(BMADInstallerError) as exc_info:
            install_bmad_headless(
                target_path=tmp_path,
                config=config
            )

        error_msg = str(exc_info.value).lower()
        assert "timeout" in error_msg or "timed out" in error_msg

    def test_unexpected_prompt_raises_error(self, mock_pexpect, tmp_path):
        """Verify unexpected prompt sequence raises error."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerError

        mock_child = MagicMock()
        mock_child.before = b"Unexpected question: What is your favorite color?"
        mock_pexpect.spawn.return_value = mock_child
        # Return index that doesn't match any known pattern (99 > num_patterns)
        mock_child.expect.return_value = 99

        config = BMADInstallerConfig()

        with pytest.raises(BMADInstallerError) as exc_info:
            install_bmad_headless(
                target_path=tmp_path,
                config=config
            )

    def test_nonzero_exit_code_returns_failure(self, mock_pexpect, tmp_path):
        """Verify non-zero exit code returns failure result."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        mock_child = MagicMock()
        mock_child.exitstatus = 1
        # EOF immediately
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig()
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        assert result.success is False
        assert result.exit_code == 1

    def test_missing_nodejs_raises_error(self, mock_pexpect, tmp_path):
        """Verify missing Node.js raises appropriate error."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerError

        mock_pexpect.spawn.side_effect = FileNotFoundError("npx not found")

        config = BMADInstallerConfig()

        with pytest.raises(BMADInstallerError) as exc_info:
            install_bmad_headless(
                target_path=tmp_path,
                config=config
            )

        assert "node" in str(exc_info.value).lower() or "npx" in str(exc_info.value).lower()


class TestBMADInstallerIdempotency:
    """Test idempotent installation behavior."""

    @pytest.fixture
    def mock_pexpect(self):
        """Mock pexpect for testing."""
        with patch("sif.bmad_installer.pexpect") as mock:
            mock.EOF = _MockEOF
            mock.TIMEOUT = _MockTIMEOUT
            mock.ExceptionPexpect = _MockExceptionPexpect
            yield mock

    def test_detects_existing_installation(self, mock_pexpect, tmp_path):
        """Verify existing BMAD installation is detected."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        # Create existing BMAD structure
        (tmp_path / "_bmad").mkdir()
        (tmp_path / "_bmad" / "bmm").mkdir()
        (tmp_path / "_bmad" / "bmm" / "config.yaml").write_text("user_name: Existing")

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # EOF immediately
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig()
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config
        )

        # Result should indicate update mode
        assert result.mode in ("update", "quick-update", "install")

    def test_preserves_existing_config(self, mock_pexpect, tmp_path):
        """Verify existing configuration is preserved on reinstall."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig

        # Create existing BMAD structure with config
        (tmp_path / "_bmad").mkdir()
        (tmp_path / "_bmad" / "bmm").mkdir()
        (tmp_path / "_bmad" / "bmm" / "config.yaml").write_text(
            "user_name: ExistingUser\ncommunication_language: Spanish"
        )

        mock_child = MagicMock()
        mock_child.exitstatus = 0
        # EOF immediately
        mock_child.expect.return_value = _get_eof_index()
        mock_pexpect.spawn.return_value = mock_child

        config = BMADInstallerConfig(user_name="NewUser")
        result = install_bmad_headless(
            target_path=tmp_path,
            config=config,
            preserve_existing=True
        )

        # Existing config should be noted
        assert result.preserved_config is not None or result.mode == "update"


class TestBMADInstallerCLI:
    """Test CLI wrapper function."""

    def test_cli_entry_point_exists(self):
        """Verify CLI entry point function exists."""
        from sif.bmad_installer import bmad_headless_install_cli
        assert callable(bmad_headless_install_cli)

    def test_cli_parses_version_flag(self):
        """Verify CLI parses --version flag correctly."""
        from sif.bmad_installer import parse_cli_args

        args = parse_cli_args(["--version", "6.0.0-Beta.5"])
        assert args.version == "6.0.0-Beta.5"

    def test_cli_parses_user_name_flag(self):
        """Verify CLI parses --user-name flag correctly."""
        from sif.bmad_installer import parse_cli_args

        args = parse_cli_args(["--user-name", "Roy"])
        assert args.user_name == "Roy"

    def test_cli_parses_language_flag(self):
        """Verify CLI parses --language flag correctly."""
        from sif.bmad_installer import parse_cli_args

        args = parse_cli_args(["--language", "Spanish"])
        assert args.language == "Spanish"

    def test_cli_parses_output_dir_flag(self):
        """Verify CLI parses --output-dir flag correctly."""
        from sif.bmad_installer import parse_cli_args

        args = parse_cli_args(["--output-dir", "_custom"])
        assert args.output_dir == "_custom"

    def test_cli_parses_debug_flag(self):
        """Verify CLI parses --debug flag correctly."""
        from sif.bmad_installer import parse_cli_args

        args = parse_cli_args(["--debug"])
        assert args.debug is True


class TestBMADInstallerPathValidation:
    """Test path validation before installation."""

    def test_nonexistent_path_raises_error(self):
        """Verify non-existent path raises appropriate error."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerError

        config = BMADInstallerConfig()

        with pytest.raises(BMADInstallerError) as exc_info:
            install_bmad_headless(
                target_path=Path("/nonexistent/path/that/does/not/exist"),
                config=config
            )

        assert "does not exist" in str(exc_info.value).lower()

    def test_file_path_raises_error(self, tmp_path):
        """Verify file path (not directory) raises appropriate error."""
        from sif.bmad_installer import install_bmad_headless, BMADInstallerConfig, BMADInstallerError

        # Create a file instead of directory
        test_file = tmp_path / "not_a_directory.txt"
        test_file.write_text("test")

        config = BMADInstallerConfig()

        with pytest.raises(BMADInstallerError) as exc_info:
            install_bmad_headless(
                target_path=test_file,
                config=config
            )

        assert "not a directory" in str(exc_info.value).lower()


class TestBMADVersionDetection:
    """Test BMAD version detection utilities."""

    def test_detect_installed_version(self, tmp_path):
        """Verify installed BMAD version can be detected."""
        from sif.bmad_installer import detect_bmad_version

        # Create mock package.json with version
        (tmp_path / "_bmad").mkdir()
        (tmp_path / "_bmad" / "package.json").write_text('{"version": "6.0.0-Beta.5"}')

        version = detect_bmad_version(tmp_path)
        assert version == "6.0.0-Beta.5"

    def test_detect_version_returns_none_if_not_installed(self, tmp_path):
        """Verify None returned if BMAD not installed."""
        from sif.bmad_installer import detect_bmad_version

        version = detect_bmad_version(tmp_path)
        assert version is None

    def test_compare_versions(self):
        """Verify version comparison works correctly."""
        from sif.bmad_installer import compare_bmad_versions

        assert compare_bmad_versions("6.0.0", "5.0.0") > 0
        assert compare_bmad_versions("6.0.0-Beta.5", "6.0.0-Beta.4") > 0
        assert compare_bmad_versions("6.0.0", "6.0.0") == 0

    def test_compare_versions_with_latest(self):
        """Verify 'latest' is handled correctly in version comparison."""
        from sif.bmad_installer import compare_bmad_versions

        assert compare_bmad_versions("latest", "6.0.0") > 0
        assert compare_bmad_versions("6.0.0", "latest") < 0
        assert compare_bmad_versions("latest", "latest") == 0

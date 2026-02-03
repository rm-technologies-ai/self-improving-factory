"""
Integration tests for provisioned project smoke testing.

These tests verify that a provisioned project can successfully use
the BMAD Quickflow agent to implement basic functionality.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import pytest


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.requires_claude
class TestProvisioningSmokeTest:
    """
    Smoke tests that verify a provisioned project works with Claude Code.

    These tests invoke the Claude CLI as a subprocess to validate that:
    1. The CLAUDE.md context is properly loaded
    2. The BMAD Quickflow agent can be invoked
    3. Basic development tasks can be completed
    """

    def test_quickflow_implements_python_hello_world(
        self,
        provisioned_test_project: Path
    ):
        """
        Test that the BMAD Quickflow agent can implement a Python hello world.

        This is an end-to-end smoke test that:
        1. Invokes Claude CLI in the provisioned test directory
        2. Prompts the Quickflow agent to implement hello world
        3. Verifies the implementation was created correctly
        """
        project_path = provisioned_test_project

        # Verify provisioning was successful
        assert (project_path / "CLAUDE.md").exists(), "CLAUDE.md not deployed"
        assert (project_path / "_bmad").exists(), "_bmad not deployed"

        # Build the prompt for the Quickflow agent
        # Using direct prompt instead of slash command for non-interactive mode
        prompt = """
You are operating as the BMAD Quick Flow Solo Dev agent.

Your task: Implement a simple Python hello world program.

Requirements:
1. Create a file called `hello.py` in the project root
2. The program should print "Hello, World!" when executed
3. Follow TDD: create a test file `tests/test_hello.py` first
4. The test should verify the output is correct

Execute this task now. Do not ask for clarification.
"""

        # Invoke Claude CLI
        result = self._invoke_claude(
            project_path=project_path,
            prompt=prompt,
            timeout=120  # 2 minutes should be sufficient
        )

        # Check Claude CLI executed successfully
        assert result.returncode == 0, f"Claude CLI failed: {result.stderr}"

        # Verify hello.py was created
        hello_py = project_path / "hello.py"
        assert hello_py.exists(), "hello.py was not created"

        # Verify hello.py content
        content = hello_py.read_text()
        assert "Hello" in content or "hello" in content, \
            f"hello.py doesn't contain hello: {content}"

        # Verify the program runs correctly
        run_result = subprocess.run(
            [sys.executable, str(hello_py)],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert run_result.returncode == 0, f"hello.py failed to run: {run_result.stderr}"
        assert "Hello" in run_result.stdout, \
            f"Output doesn't contain Hello: {run_result.stdout}"

    def test_quickflow_with_slash_command(
        self,
        provisioned_test_project: Path
    ):
        """
        Test invoking Quickflow via slash command style prompt.

        This tests the native context window with BMAD agent invocation.
        """
        project_path = provisioned_test_project

        # Prompt that references the quickflow agent activation
        prompt = """
Load and activate the quick-flow-solo-dev agent from _bmad/bmm/agents/quick-flow-solo-dev.md.

Once activated, execute option 5 (Quick Dev) with this task:
"Create a Python function in utils.py that adds two numbers and returns the result."

Do not display menus or wait for input. Execute autonomously.
"""

        result = self._invoke_claude(
            project_path=project_path,
            prompt=prompt,
            timeout=120
        )

        assert result.returncode == 0, f"Claude CLI failed: {result.stderr}"

        # Verify utils.py was created with add function
        utils_py = project_path / "utils.py"
        assert utils_py.exists(), "utils.py was not created"

        content = utils_py.read_text()
        assert "def " in content, "No function definition found"
        assert "add" in content.lower() or "sum" in content.lower(), \
            "Add function not found"

    def _invoke_claude(
        self,
        project_path: Path,
        prompt: str,
        timeout: int = 120,
        model: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """
        Invoke Claude CLI as a subprocess.

        Args:
            project_path: Directory to run Claude in
            prompt: The prompt to send
            timeout: Timeout in seconds
            model: Optional model override

        Returns:
            CompletedProcess with stdout, stderr, returncode
        """
        cmd = ["claude", "--print"]

        if model:
            cmd.extend(["--model", model])

        # Add the prompt
        cmd.extend(["--prompt", prompt])

        # Set up environment
        env = os.environ.copy()
        env["CLAUDE_CODE_ENTRYPOINT"] = "cli"

        try:
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            return result
        except subprocess.TimeoutExpired as e:
            # Return a failed result on timeout
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=1,
                stdout=e.stdout or "",
                stderr=f"Timeout after {timeout}s: {e.stderr or ''}"
            )
        except FileNotFoundError:
            pytest.skip("Claude CLI not found - install with: npm install -g @anthropic-ai/claude-code")


@pytest.mark.integration
@pytest.mark.bmad_installer
class TestBMADInstallerMode:
    """
    Tests that use the real BMAD installer (npx bmad-method install).

    These tests are skipped until REQ-024 (Headless BMAD Wrapper) is implemented.
    The upstream BMAD installer is interactive and requires user prompts.

    See: https://github.com/bmad-code-org/BMAD-METHOD
    """

    def test_bmad_installer_creates_structure(
        self,
        provisioned_test_project: Path
    ):
        """
        Test that real BMAD installer creates expected structure.

        This test uses `npx bmad-method install` via the headless wrapper.
        """
        project_path = provisioned_test_project

        # Verify BMAD structure created by installer
        assert (project_path / "_bmad").exists()
        assert (project_path / ".claude" / "commands").exists()

        # Verify config file
        config_file = project_path / "_bmad" / "bmm" / "config.yaml"
        assert config_file.exists()

    def test_bmad_installer_version_pinning(
        self,
        clean_test_project: Path
    ):
        """
        Test that specific BMAD version can be installed.

        Uses: npx bmad-method@6.0.0-Beta.5 install
        """
        # This test will be implemented with REQ-024
        pytest.skip("Requires REQ-024 (headless wrapper)")


@pytest.mark.integration
class TestProvisioningStructure:
    """
    Tests that verify the provisioned project structure is correct.

    These are faster tests that don't require Claude CLI invocation.
    """

    def test_claude_md_deployed(self, provisioned_test_project: Path):
        """Verify CLAUDE.md is deployed correctly."""
        claude_md = provisioned_test_project / "CLAUDE.md"
        assert claude_md.exists()

        content = claude_md.read_text()
        assert "Production Enterprise Grade" in content
        assert "SOLID Principles" in content
        assert "TDD Principles" in content

    def test_bmad_structure_deployed(self, provisioned_test_project: Path):
        """Verify _bmad structure is deployed."""
        bmad_dir = provisioned_test_project / "_bmad"
        assert bmad_dir.exists()
        assert bmad_dir.is_dir()

        # Check for key BMAD components
        agents_dir = bmad_dir / "bmm" / "agents"
        assert agents_dir.exists(), "_bmad/bmm/agents not found"

        quickflow_agent = agents_dir / "quick-flow-solo-dev.md"
        assert quickflow_agent.exists(), "quick-flow-solo-dev.md agent not found"

    def test_claude_commands_deployed(self, provisioned_test_project: Path):
        """Verify .claude/commands are deployed for slash commands."""
        commands_dir = provisioned_test_project / ".claude" / "commands"
        assert commands_dir.exists()

        # Check for quickflow command
        quickflow_cmd = commands_dir / "bmad-agent-bmm-quick-flow-solo-dev.md"
        assert quickflow_cmd.exists()

    def test_bmad_output_directory_exists(self, provisioned_test_project: Path):
        """Verify _bmad-output directory is created."""
        bmad_output = provisioned_test_project / "_bmad-output"
        assert bmad_output.exists()
        assert bmad_output.is_dir()

    def test_git_initialized(self, provisioned_test_project: Path):
        """Verify git is initialized in the test project."""
        git_dir = provisioned_test_project / ".git"
        assert git_dir.exists()
        assert git_dir.is_dir()

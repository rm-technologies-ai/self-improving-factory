"""
Pytest configuration and fixtures for self-improving-factory tests.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Generator

import pytest


# Test project location (as defined in project state)
TEST_PROJECT_PATH = Path.home() / "repos" / "test-project"

# Factory project root
FACTORY_ROOT = Path(__file__).parent.parent

# rm-claude-code library path
RM_CLAUDE_CODE_PATH = Path.home() / "repos" / "rm-claude-code"


@pytest.fixture
def test_project_path() -> Path:
    """Return the test project path."""
    return TEST_PROJECT_PATH


@pytest.fixture
def factory_root() -> Path:
    """Return the factory project root."""
    return FACTORY_ROOT


@pytest.fixture
def rm_claude_code_path() -> Path:
    """Return the rm-claude-code library path."""
    return RM_CLAUDE_CODE_PATH


@pytest.fixture
def clean_test_project(test_project_path: Path) -> Generator[Path, None, None]:
    """
    Fixture that provides a clean test project directory.

    Teardown protocol (from project state):
    - Delete everything locally EXCEPT the project folder
    - Preserves folder structure for rapid dev/test cycles
    """
    # Ensure directory exists
    test_project_path.mkdir(parents=True, exist_ok=True)

    # Clean contents but preserve folder
    for item in test_project_path.iterdir():
        if item.name == ".git":
            continue  # Optionally preserve git
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    yield test_project_path

    # Teardown: clean again but preserve folder
    for item in test_project_path.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


@pytest.fixture
def provisioned_test_project(
    clean_test_project: Path,
    rm_claude_code_path: Path,
    factory_root: Path
) -> Generator[Path, None, None]:
    """
    Fixture that provides a provisioned test project with CLAUDE.md and BMAD.

    This simulates the provisioning process by copying:
    - CLAUDE.md from rm-claude-code production-enterprise-grade variant
    - _bmad/ structure from factory
    - .claude/commands/ for slash commands
    """
    project_path = clean_test_project
    variant_path = rm_claude_code_path / "variants" / "production-enterprise-grade"

    # Deploy CLAUDE.md
    claude_md_src = variant_path / "CLAUDE.md"
    if claude_md_src.exists():
        shutil.copy(claude_md_src, project_path / "CLAUDE.md")

    # Deploy CLAUDE-ADD.md template
    claude_add_src = variant_path / "templates" / "CLAUDE-ADD.md"
    if claude_add_src.exists():
        shutil.copy(claude_add_src, project_path / "CLAUDE-ADD.md")

    # Deploy _bmad/ structure
    bmad_src = factory_root / "_bmad"
    if bmad_src.exists():
        shutil.copytree(bmad_src, project_path / "_bmad")

    # Deploy .claude/commands/ for slash commands
    claude_commands_src = factory_root / ".claude" / "commands"
    if claude_commands_src.exists():
        (project_path / ".claude").mkdir(exist_ok=True)
        shutil.copytree(claude_commands_src, project_path / ".claude" / "commands")

    # Create _bmad-output/ directory
    (project_path / "_bmad-output").mkdir(exist_ok=True)

    # Initialize git if not exists
    if not (project_path / ".git").exists():
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            check=True
        )

    yield project_path


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (may invoke external processes)"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers",
        "requires_claude: mark test as requiring Claude CLI"
    )

import os
import shutil
from argparse import Namespace
from unittest.mock import patch

import pytest

from uv_init.__main__ import initialize_uv_project


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project creation"""
    project_dir = tmp_path / "test-projects"
    project_dir.mkdir()

    # Store the temp directory path in the environment variable
    os.environ["UV_ORIGINAL_CWD"] = str(project_dir)

    yield project_dir

    # Cleanup
    if project_dir.exists():
        try:
            shutil.rmtree(project_dir)
        except Exception as e:  # noqa: BLE001
            print(f"Cleanup failed: {e}")

    # Clean up environment
    if "UV_ORIGINAL_CWD" in os.environ:
        del os.environ["UV_ORIGINAL_CWD"]


def test_basic_lib_project(temp_project_dir):
    """Test creating a basic library project"""
    project_name = "test-lib"
    project_path = temp_project_dir / project_name

    args = Namespace(
        project_name=project_name,
        type="lib",
        python="3.12",
        workspace=False,
        github=False,
    )

    initialize_uv_project(args)

    # Verify basic project structure
    assert (project_path / "src" / "test_lib").exists(), (
        "Source directory not created"
    )
    assert (project_path / "pyproject.toml").exists(), (
        "pyproject.toml not created"
    )
    assert (project_path / "tests").exists(), "Tests directory not created"
    assert (project_path / "README.md").exists(), "README.md not created"
    assert (project_path / ".gitignore").exists(), ".gitignore not created"
    assert (project_path / "LICENSE").exists(), "LICENSE file not created"
    assert (project_path / ".pre-commit-config.yaml").exists(), (
        "Pre-commit config not created"
    )

    # Verify lib-specific content
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert 'name = "test-lib"' in pyproject_content, (
        "Project name not correctly set in pyproject.toml"
    )
    assert 'python = ">=3.12"' in pyproject_content, (
        "Python version not correctly set in pyproject.toml"
    )

    # Verify dev dependencies configuration
    assert "[tool.ruff]" in pyproject_content, (
        "Ruff configuration missing in pyproject.toml"
    )
    assert "[tool.pytest.ini_options]" in pyproject_content, (
        "Pytest configuration missing in pyproject.toml"
    )
    assert "[tool.ty]" in pyproject_content, (
        "Ty configuration missing in pyproject.toml"
    )
    assert "[tool.commitizen]" in pyproject_content, (
        "Commitizen configuration missing in pyproject.toml"
    )

    # Verify version file
    init_content = (
        project_path / "src" / "test_lib" / "__init__.py"
    ).read_text()
    assert any(
        version in init_content
        for version in ['__version__ = "0.1.0"', "__version__ = '0.1.0'"]
    ), "Version string not found in __init__.py"

    # Verify README content
    readme_content = (project_path / "README.md").read_text()
    assert "Python 3.12" in readme_content, (
        "Python version not found in README"
    )
    assert "test-lib" in readme_content, "Project name not found in README"


def test_basic_app_project(temp_project_dir):
    """Test creating a basic application project"""
    project_name = "test-app"
    project_path = temp_project_dir / project_name

    args = Namespace(
        project_name=project_name,
        type="app",
        python="3.12",
        workspace=False,
        github=False,
    )

    initialize_uv_project(args)

    # Verify app project structure
    assert (project_path / "src" / "test_app").exists(), (
        "Source directory not created"
    )
    assert (project_path / "pyproject.toml").exists(), (
        "pyproject.toml not created"
    )
    assert (project_path / "tests").exists(), "Tests directory not created"
    assert (project_path / "README.md").exists(), "README.md not created"
    assert (project_path / ".gitignore").exists(), ".gitignore not created"
    assert (project_path / "LICENSE").exists(), "LICENSE file not created"
    assert (project_path / ".pre-commit-config.yaml").exists(), (
        "Pre-commit config not created"
    )

    # Verify app-specific content
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert 'name = "test-app"' in pyproject_content, (
        "Project name not correctly set in pyproject.toml"
    )
    assert 'python = ">=3.12"' in pyproject_content, (
        "Python version not correctly set in pyproject.toml"
    )

    # Verify dev dependencies configuration
    assert "[tool.ruff]" in pyproject_content, (
        "Ruff configuration missing in pyproject.toml"
    )
    assert "[tool.pytest.ini_options]" in pyproject_content, (
        "Pytest configuration missing in pyproject.toml"
    )
    assert "[tool.ty]" in pyproject_content, (
        "Ty configuration missing in pyproject.toml"
    )
    assert "[tool.commitizen]" in pyproject_content, (
        "Commitizen configuration missing in pyproject.toml"
    )

    # Verify version file
    init_content = (
        project_path / "src" / "test_app" / "__init__.py"
    ).read_text()
    assert any(
        version in init_content
        for version in ['__version__ = "0.1.0"', "__version__ = '0.1.0'"]
    ), "Version string not found in __init__.py"


def test_workspace_project(temp_project_dir):
    """Test creating a workspace project"""
    project_name = "test-workspace"
    project_path = temp_project_dir / project_name

    args = Namespace(
        project_name=project_name,
        type="lib",
        python="3.12",
        workspace=True,
        github=False,
    )

    with patch(
        "rich.prompt.Prompt.ask", side_effect=["y", "common_utils", "n"]
    ):
        initialize_uv_project(args)

    # Verify workspace structure
    assert (project_path / "packages").exists(), (
        "Packages directory not created"
    )
    assert (project_path / "pyproject.toml").exists(), (
        "pyproject.toml not created"
    )
    assert (project_path / "README.md").exists(), "README.md not created"
    assert (project_path / ".gitignore").exists(), ".gitignore not created"
    assert (project_path / "LICENSE").exists(), "LICENSE file not created"
    assert (project_path / ".pre-commit-config.yaml").exists(), (
        "Pre-commit config not created"
    )

    # Verify workspace-specific content
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert 'name = "test-workspace"' in pyproject_content, (
        "Project name not correctly set in pyproject.toml"
    )
    assert "[tool.uv.workspace]" in pyproject_content, (
        "Workspace configuration missing in pyproject.toml"
    )
    assert "[tool.uv.sources]" in pyproject_content, (
        "Sources configuration missing in pyproject.toml"
    )

    # Verify dev dependencies configuration
    assert "[tool.ruff]" in pyproject_content, (
        "Ruff configuration missing in pyproject.toml"
    )
    assert "[tool.pytest.ini_options]" in pyproject_content, (
        "Pytest configuration missing in pyproject.toml"
    )
    assert "[tool.ty]" in pyproject_content, (
        "Ty configuration missing in pyproject.toml"
    )
    assert "[tool.commitizen]" in pyproject_content, (
        "Commitizen configuration missing in pyproject.toml"
    )

    # Verify README content
    readme_content = (project_path / "README.md").read_text()
    assert "test-workspace" in readme_content, (
        "Project name not found in README"
    )


def test_project_with_different_python(temp_project_dir):
    """Test creating a project with different Python version"""
    project_name = "test-python"
    project_path = temp_project_dir / project_name

    args = Namespace(
        project_name=project_name,
        type="lib",
        python="3.11",
        workspace=False,
        github=False,
    )

    initialize_uv_project(args)

    # Verify Python version in configs
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert 'python = ">=3.11"' in pyproject_content

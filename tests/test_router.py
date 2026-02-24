import subprocess
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from uv_init.exceptions import ProjectCreationError
from uv_init.router import CommandDispatcher


@pytest.fixture
def temp_cwd(tmp_path):
    """Create a temporary working directory"""
    project_dir = tmp_path / "test-project"
    tests_dir = project_dir / "tests"
    project_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)
    return tmp_path


@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls"""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0)
        yield mock_run


@pytest.fixture
def mock_rprint():
    """Mock rich.print"""
    with patch("uv_init.router.rprint") as mock_print:
        yield mock_print


@pytest.fixture
def base_args():
    return Namespace(
        project_name="test-project",
        python="3.12",
        workspace=False,
    )


@pytest.fixture
def mock_fs():
    """Mock all filesystem operations"""
    with (
        patch("pathlib.Path.exists", return_value=True) as mock_exists,
        patch("pathlib.Path.mkdir", return_value=None) as mock_mkdir,
        patch("pathlib.Path.is_dir", return_value=True) as mock_is_dir,
        patch(
            "pathlib.Path.absolute", return_value=Path("/fake/path")
        ) as mock_abs,
    ):
        yield {
            "exists": mock_exists,
            "mkdir": mock_mkdir,
            "is_dir": mock_is_dir,
            "absolute": mock_abs,
        }


@pytest.fixture
def dispatcher(base_args, temp_cwd, mock_fs):
    """Create a CommandDispatcher instance"""
    return CommandDispatcher(base_args, temp_cwd)


def test_lib_project(mock_subprocess, dispatcher, base_args, mock_fs):
    """Test creating a library project"""
    base_args.type = "lib"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        ["uv", "init", "test-project", "--lib", "--python", "3.12"],
        check=True,
        cwd=dispatcher.original_cwd,
    )


def test_package_project(mock_subprocess, dispatcher, base_args, mock_fs):
    """Test creating a package project"""
    base_args.type = "package"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        ["uv", "init", "test-project", "--package", "--python", "3.12"],
        check=True,
        cwd=dispatcher.original_cwd,
    )


def test_invalid_project_type(base_args, temp_cwd, mock_fs):
    """Test handling invalid project type"""
    args = base_args
    args.type = "invalid"

    dispatcher = CommandDispatcher(args, temp_cwd)
    with pytest.raises(ValueError, match="Unknown project type: invalid"):
        dispatcher.dispatch()


def test_subprocess_error(mock_subprocess, base_args, temp_cwd, mock_fs):
    """Test handling subprocess error"""
    args = base_args
    args.type = "lib"

    error = subprocess.CalledProcessError(1, ["uv", "init"])
    mock_subprocess.side_effect = error

    dispatcher = CommandDispatcher(args, temp_cwd)
    with pytest.raises(ProjectCreationError):
        dispatcher.dispatch()

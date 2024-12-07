import subprocess
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from uv_init.router import CommandDispatcher


@pytest.fixture
def temp_cwd(tmp_path):
    """Create a temporary working directory"""
    return tmp_path


@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls"""
    with patch("subprocess.run") as mock_run:
        # Configure the mock to return a successful result by default
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
def dispatcher(base_args):
    """Create a CommandDispatcher instance"""
    return CommandDispatcher(base_args, Path.cwd())


def test_lib_project(mock_subprocess, dispatcher, base_args):
    """Test creating a library project"""
    base_args.type = "lib"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        ["uv", "init", "test-project", "--lib", "--python", "3.12"],
        check=True,
        cwd=Path.cwd(),
    )


def test_app_project(mock_subprocess, dispatcher, base_args):
    """Test creating an application project"""
    base_args.type = "app"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        ["uv", "init", "test-project", "--app", "--python", "3.12"],
        check=True,
        cwd=Path.cwd(),
    )


def test_package_project(mock_subprocess, dispatcher, base_args):
    """Test creating a package project"""
    base_args.type = "package"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        ["uv", "init", "test-project", "--package", "--python", "3.12"],
        check=True,
        cwd=Path.cwd(),
    )


def test_full_project(mock_subprocess, dispatcher, base_args):
    """Test creating a full project (package + app)"""
    base_args.type = "full"
    dispatcher.dispatch()

    mock_subprocess.assert_called_once_with(
        [
            "uv",
            "init",
            "test-project",
            "--package",
            "--app",
            "--python",
            "3.12",
        ],
        check=True,
        cwd=Path.cwd(),
    )


def test_invalid_project_type(base_args):
    """Test handling invalid project type"""
    args = base_args
    args.type = "invalid"

    dispatcher = CommandDispatcher(args, Path.cwd())
    with pytest.raises(ValueError, match="Unknown project type: invalid"):
        dispatcher.dispatch()


def test_subprocess_error(mock_subprocess, base_args):
    """Test handling subprocess error"""
    args = base_args
    args.type = "lib"

    # Create a CalledProcessError instance correctly
    error = subprocess.CalledProcessError(1, ["uv", "init"])
    mock_subprocess.side_effect = error

    dispatcher = CommandDispatcher(args, Path.cwd())
    with pytest.raises(SystemExit):
        dispatcher.dispatch()

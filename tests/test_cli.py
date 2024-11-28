from argparse import ArgumentTypeError
from unittest.mock import patch

import pytest

from uv_init.cli import parse_args, validate_project_name


def test_validate_project_name_valid():
    assert validate_project_name("validname") == "validname"
    assert validate_project_name("valid-name") == "valid-name"
    assert validate_project_name("valid123") == "valid123"

def test_validate_project_name_with_space():
    with pytest.raises(ArgumentTypeError) as exc:
        validate_project_name("invalid name")
    assert "cannot contain spaces" in str(exc.value)


def test_validate_project_name_with_underscore():
    with pytest.raises(ArgumentTypeError) as exc:
        validate_project_name("invalid_name")
    assert "cannot contain spaces or under-scores" in str(exc.value)

# Test argument parsing
def test_parse_args_defaults(capsys):
    """Test parsing arguments with defaults"""
    with patch("sys.argv", ["uv-init", "my-project"]):
        args = parse_args()
        assert args.project_name == "my-project"
        assert args.type == "lib"  # Default type should be lib
        assert args.python == "3.12"
        assert args.workspace is False

def test_parse_args_with_options(capsys):
    """Test parsing arguments with options"""
    with patch("sys.argv", [
        "uv-init",
        "my-project",
        "--type", "app",
        "--python", "3.11",
        "--workspace"
    ]):
        args = parse_args()
        assert args.project_name == "my-project"
        assert args.type == "app"
        assert args.python == "3.11"
        assert args.workspace is True

def test_parse_args_invalid_type(monkeypatch):
    # Simulate invalid project type
    monkeypatch.setattr(
        "sys.argv", ["program", "validname", "--type", "invalid"]
    )
    with pytest.raises(SystemExit):
        parse_args()
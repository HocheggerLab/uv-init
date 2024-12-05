import shutil
from argparse import Namespace
from pathlib import Path

import pytest

from src.uv_init.parse_docs import (
    _copy_template,
    load_env_data,
    _update_content,
)


@pytest.fixture
def temp_project_structure(tmp_path):
    """Create a temporary project structure with template files.

    Returns:
        tuple: (project_dir, template_dir) paths
    """
    # Create template directory
    template_dir = tmp_path / "template"
    template_dir.mkdir()

    # Create project directory
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    # Create sample template files
    (template_dir / "README.md").write_text("# Sample README")
    (template_dir / "LICENSE").write_text("Sample License")
    (template_dir / ".gitignore").write_text("*.pyc\n__pycache__/")

    # Monkeypatch cwd to our temp directory
    with pytest.MonkeyPatch().context() as mp:
        mp.chdir(tmp_path)
        yield project_dir, template_dir

    # Cleanup happens automatically thanks to tmp_path


def test_copy_template_success(temp_project_structure):
    """Test successful template file copying."""
    project_dir, _ = temp_project_structure

    # Test copying each template file
    for template in ["README.md", "LICENSE", ".gitignore"]:
        _copy_template(template, project_dir)
        assert (project_dir / template).exists()
        assert (project_dir / template).read_text() == (
            Path.cwd() / f"template/{template}"
        ).read_text()


def test_copy_template_file_not_found(temp_project_structure):
    """Test handling of missing template file."""
    project_dir, _ = temp_project_structure

    with pytest.raises(SystemExit):
        _copy_template("nonexistent.txt", project_dir)


def test_load_env_data(monkeypatch, tmp_path):
    """Test loading environment variables from a mocked .env file."""
    # Create a temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text(
        "AUTHOR_NAME=Test Author\nAUTHOR_EMAIL=test@example.com"
    )

    # Monkeypatch the environment to load from the temporary .env file
    monkeypatch.setenv("AUTHOR_NAME", "Test Author")
    monkeypatch.setenv("AUTHOR_EMAIL", "test@example.com")

    # Load the environment data
    env_data = load_env_data()

    # Assert the environment variables are loaded correctly
    assert env_data["AUTHOR_NAME"] == "Test Author"
    assert env_data["AUTHOR_EMAIL"] == "test@example.com"


def test_update_content(tmp_path: Path):
    # Setup temporary project directory and files
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    for template in ["README.md", "LICENSE"]:
        # Copy actual template file to temp path
        template_file = Path.cwd() / f"template/{template}"
        shutil.copy(template_file, project_dir / template)

    # Define args
    args = Namespace(project_name="TestProject", python="3.9")

    # Call the function
    _update_content(project_dir, args)

    # Check README.md content
    readme_path = project_dir / "README.md"
    readme_content = readme_path.read_text()

    # Verify replacements
    assert "# TestProject" in readme_content
    assert "Python 3.9" in readme_content
    assert "Helfrid" in readme_content  # Default author name
    assert "hh65" in readme_content  # Default email

    # Check LICENSE content
    license_content = (project_dir / "LICENSE").read_text()
    assert "Helfrid" in license_content

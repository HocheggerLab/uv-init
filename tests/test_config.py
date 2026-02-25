"""Tests for uv_init.config module."""

from unittest.mock import patch

from uv_init.config import (
    _git_config,
    load_config,
    save_config,
)


def test_load_config_from_file(tmp_path, monkeypatch):
    """Test loading config from a TOML file."""
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        '[user]\nname = "Jane Doe"\nemail = "jane@example.com"\n'
    )
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    config = load_config()
    assert config.author_name == "Jane Doe"
    assert config.author_email == "jane@example.com"


def test_load_config_fallback_to_git(tmp_path, monkeypatch):
    """Test fallback to git config when no config file exists."""
    config_file = tmp_path / "nonexistent.toml"
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    with patch("uv_init.config._git_config") as mock_git:
        mock_git.side_effect = lambda key: {
            "user.name": "Git User",
            "user.email": "git@example.com",
        }.get(key)

        config = load_config()
        assert config.author_name == "Git User"
        assert config.author_email == "git@example.com"


def test_load_config_fallback_to_defaults(tmp_path, monkeypatch):
    """Test fallback to defaults when no config file or git config."""
    config_file = tmp_path / "nonexistent.toml"
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    with patch("uv_init.config._git_config", return_value=None):
        config = load_config()
        assert config.author_name == "Unknown"
        assert config.author_email == "unknown@example.com"


def test_load_config_partial_git(tmp_path, monkeypatch):
    """Test fallback when git has name but not email."""
    config_file = tmp_path / "nonexistent.toml"
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    with patch("uv_init.config._git_config") as mock_git:
        mock_git.side_effect = lambda key: {
            "user.name": "Git User",
            "user.email": None,
        }.get(key)

        config = load_config()
        assert config.author_name == "Git User"
        assert config.author_email == "unknown@example.com"


def test_save_config(tmp_path, monkeypatch):
    """Test saving config writes valid TOML."""
    config_dir = tmp_path / "uv-init"
    config_file = config_dir / "config.toml"
    monkeypatch.setattr("uv_init.config.CONFIG_DIR", config_dir)
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    save_config(name="Test User", email="test@example.com")

    assert config_file.exists()
    content = config_file.read_text()
    assert 'name = "Test User"' in content
    assert 'email = "test@example.com"' in content


def test_save_then_load(tmp_path, monkeypatch):
    """Test round-trip: save then load."""
    config_dir = tmp_path / "uv-init"
    config_file = config_dir / "config.toml"
    monkeypatch.setattr("uv_init.config.CONFIG_DIR", config_dir)
    monkeypatch.setattr("uv_init.config.CONFIG_FILE", config_file)

    save_config(name="Round Trip", email="rt@example.com")
    config = load_config()

    assert config.author_name == "Round Trip"
    assert config.author_email == "rt@example.com"


def test_git_config_returns_none_when_git_missing():
    """Test _git_config returns None when git is not installed."""
    with patch(
        "uv_init.config.subprocess.run",
        side_effect=FileNotFoundError,
    ):
        assert _git_config("user.name") is None


def test_git_config_returns_none_for_empty_value():
    """Test _git_config returns None when git config key is unset."""
    with patch("uv_init.config.subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        assert _git_config("user.name") is None

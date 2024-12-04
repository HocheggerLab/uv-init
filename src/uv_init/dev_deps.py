import subprocess
from pathlib import Path

from rich import print as rprint
from rich.panel import Panel


def add_dev_dependencies(project_name: str, project_path: Path) -> None:
    """Add dev dependencies to the project"""
    try:
        # Add development dependencies
        result = subprocess.run(
            ["uv", "add", "--dev", "ruff", "pytest", "mypy", "commitizen"],
            check=True,
            cwd=project_path
        )

        if result.returncode == 0:
            rprint("[green]Development dependencies added successfully.[/green]")
        else:
            raise subprocess.CalledProcessError(result.returncode, result.args)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to add development dependencies\n{e}",
                title="Dependency Addition Failed",
                border_style="red",
            )
        )
        exit(1)

def parse_dev_configs(project_path: Path) -> None:
    """Parse dev configs from the project directory"""
    config_dir = Path.cwd() / "template"
    config_files = [
        config_dir / "mypy-config.toml",
        config_dir / "ruff-config.toml",
        config_dir / "pytest-config.toml",
        config_dir / "commitizen-config.toml",
    ]
    pyproject_toml_list = [project_path / "pyproject.toml"] + (
        [
            package / "pyproject.toml"
            for package in (project_path / "packages").iterdir()
            if package.is_dir()
        ]
        if (project_path / "packages").exists()
        else []
    )

    try:
        for pyproject_toml in pyproject_toml_list:
            with pyproject_toml.open("a") as pyproject_file:
                for config_file in config_files:
                    if config_file.exists():
                        with config_file.open("r") as config_file_content:
                            pyproject_file.write(f"\n{config_file_content.read()}\n")
        rprint(
            f"[green]Added config files to pyproject[/green]"
        )
                    
    except FileNotFoundError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] pyproject.toml not found\n{e}",
                title="Pyproject.toml Not Found",
                border_style="red",
            )
        )
        exit(1)
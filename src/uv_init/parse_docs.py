"""Module to copy the README.md file to the build directory and add author information."""

import glob
import os
import shutil
from argparse import Namespace
from pathlib import Path

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel


def parse_docs(args: Namespace, project_dir: Path) -> None:
    """Parse the README.md file and update the content with project information."""
    for template in ["README.md", "LICENSE", ".gitignore"]:
        copy_template(template, project_dir)
    update_readme(project_dir, args)
    update_license(project_dir, args)
    init_version(args, project_dir)
    pyproject_package_name(args, project_dir)


def copy_template(template: str, project_dir: Path) -> None:
    """Copy template files to the build directory"""
    try:
        copy_path = Path.cwd() / f"template/{template}"
        paste_path = project_dir / f"{template}"
        shutil.copy(copy_path, paste_path)
        rprint(f"[green]{template} copied to root project[/green]")
        if template == "README.md" and (project_dir / "packages").exists():
            for package in (project_dir / "packages").iterdir():
                if package.is_dir():
                    shutil.copy(copy_path, package)
            rprint(f"[green]{template} successfully copied[/green]")
    except FileNotFoundError:
        rprint(
            Panel.fit(
                "[red]{template} not found[/red]",
                title="{template}} Template Not Found",
                border_style="red",
            )
        )
        exit(1)


def load_env_data() -> dict:
    """Load environment variables from .env file.

    Returns:
        dict: Dictionary containing environment variables
    """
    load_dotenv()
    return {
        "AUTHOR_NAME": os.getenv("AUTHOR_NAME", "Unknown"),
        "AUTHOR_EMAIL": os.getenv("AUTHOR_EMAIL", "No email provided"),
    }


def update_readme(project_dir: Path, args: Namespace) -> None:
    """Update the README.md and LICENSE content with project information.

    Args:
        project_dir: Path to the project directory
        args: Dictionary containing project configuration (from argparse)
    """
    env_data = load_env_data()
    try:
        readme_path = [project_dir / "README.md"] + (
            [
                package / "README.md"
                for package in (project_dir / "packages").iterdir()
                if package.is_dir()
            ]
            if (project_dir / "packages").exists()
            else []
        )

        # Update README.md
        for readme in readme_path:
            with readme.open("r") as f:
                content = f.read()
            parent_dir_name = readme.parent.name
            readme_replacements = {
                "# Title": f"# {parent_dir_name}",
                "{project_name}": parent_dir_name,
                "{python_version}": args.python,
                "{author}": env_data.get("AUTHOR_NAME", "Unknown"),
                "{email}": env_data.get("AUTHOR_EMAIL", "No email provided"),
            }

            for old, new in readme_replacements.items():
                content = content.replace(old, new)

            with readme.open("w") as f:
                f.write(content)
        rprint("[green]README.md successfully updated[/green]")

    except FileNotFoundError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to update README.md\n{e}",
                title="README.md not updated",
                border_style="red",
            )
        )
        exit(1)


def update_license(project_dir: Path, args: Namespace) -> None:
    """Update the LICENSE content with project information."""
    env_data = load_env_data()
    try:
        license_path = project_dir / "LICENSE"
        # Update LICENSE
        with license_path.open("r") as f:
            license_content = f.read()
            license_content = license_content.replace(
                "{author}", env_data.get("AUTHOR_NAME", "Unknown")
            )

        with license_path.open("w") as f:
            f.write(license_content)
        rprint("[green]LICENSE updated[/green]")
    except FileNotFoundError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to update LICENSE\n{e}",
                title="LICENCE Not Found",
                border_style="red",
            )
        )
        exit(1)


def init_version(args: Namespace, project_dir: Path) -> None:
    """Initialize the version file with the initial version."""
    try:
        package_name = args.project_name.replace("-", "_")
        package_path = [project_dir / "src" / package_name / "__init__.py"]
        if (project_dir / "packages").exists():
            for sub_package in (project_dir / "packages").iterdir():
                sub_package_name = sub_package.name.replace("-", "_")
                package_path.append(
                    sub_package / f"src/{sub_package_name}/__init__.py"
                )
        for version_path in package_path:
            with version_path.open("w") as f:
                f.write("__version__ = '0.1.0'")
            rprint(
                f"[green]Version file initialized for {version_path}[/green]"
            )
    except FileNotFoundError:
        rprint(
            Panel.fit(
                "[red]Version file not found[/red]",
                title="Version File Not Found",
                border_style="red",
            )
        )
        exit(1)


def pyproject_package_name(args: Namespace, project_dir: Path) -> None:
    """Update the pyproject.toml commitizen package path with the underscored package name."""
    try:
        pyproject_paths = [project_dir / "pyproject.toml"] + (
            [
                package / "pyproject.toml"
                for package in (project_dir / "packages").iterdir()
                if package.is_dir()
            ]
            if (project_dir / "packages").exists()
            else []
        )

        for pyproject_path in pyproject_paths:
            package_name = pyproject_path.parent.name.replace("-", "_")
            # Read the existing content of pyproject.toml
            with pyproject_path.open("r") as f:
                content = f.read()

            # Replace {package_name} with the actual package name
            content = content.replace("{package_name}", package_name)

            # Write the updated content back to pyproject.toml
            with pyproject_path.open("w") as f:
                f.write(content)
            rprint(
                f"[green]pyproject.toml updated for {pyproject_path}[/green]"
            )
    except FileNotFoundError:
        rprint(
            Panel.fit(
                "[red]pyproject.toml file not found[/red]",
                title="pyproject.toml Not Found",
                border_style="red",
            )
        )
        exit(1)

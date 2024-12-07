"""
Module to copy the README.md, LICENCE, .gitignore and .pre-commit-config.yaml files
to the build directory and add author information.
"""

import os
import shutil
from argparse import Namespace
from pathlib import Path

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel


def parse_docs(args: Namespace, project_dir: Path) -> None:
    """Parse the README.md file and update the content with project information."""
    for template in [
        "README.md",
        "LICENSE",
        ".gitignore",
        ".pre-commit-config.yaml",
    ]:
        _copy_template(template, project_dir)
    if args.github:
        _add_github_workflows(project_dir)
    _update_configs(project_dir, args)
    _init_version(args, project_dir)


def _copy_template(template: str, project_dir: Path) -> None:
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


def _update_configs(project_dir: Path, args: Namespace) -> None:
    """Update the configuration files with project information."""
    for template in ["README.md", "LICENSE", "pyproject.toml"]:
        _update_content(project_dir, args, template)


def _parse_replacement(args: Namespace, content_path: Path) -> dict[str, str]:
    """Load replacements for the README.md files into dictionary."""
    load_dotenv()

    AUTHOR_NAME = os.getenv("AUTHOR_NAME", "Unknown")
    AUTHOR_EMAIL = os.getenv("AUTHOR_EMAIL", "No email provided")

    parent_dir_name = content_path.parent.name
    return {
        "# Title": f"# {parent_dir_name}",
        "{project_name}": parent_dir_name,
        "{python_version}": args.python,
        "{author}": AUTHOR_NAME,
        "{email}": AUTHOR_EMAIL,
        "{package_name}": parent_dir_name,
        "v$version": f"{parent_dir_name}-v$version",
    }


def _update_content(
    project_dir: Path, args: Namespace, content_type: str
) -> None:
    """Update the content of a file with project information."""
    try:
        content_path = [project_dir / content_type] + (
            [
                package / content_type
                for package in (project_dir / "packages").iterdir()
                if package.is_dir()
            ]
            if (project_dir / "packages").exists()
            and content_type != "LICENSE"
            else []
        )
        for file in content_path:
            replacements = _parse_replacement(args, file)
            with file.open("r") as f:
                content = f.read()
            for old, new in replacements.items():
                content = content.replace(old, new)
            with file.open("w") as f:
                f.write(content)
        rprint(f"[green]{content_type} successfully updated[/green]")
    except FileNotFoundError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to update {content_type}\n{e}",
                title=f"{content_type} not updated",
                border_style="red",
            )
        )
        exit(1)


def _init_version(args: Namespace, project_dir: Path) -> None:
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


def _add_github_workflows(project_dir: Path) -> None:
    """Add GitHub workflow configurations to the project."""
    try:
        # Create .github/workflows directory
        workflows_dir = project_dir / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Copy workflow files
        for workflow in ["ci.yml", "release.yml"]:
            source = (
                Path.cwd() / "template" / ".github" / "workflows" / workflow
            )
            dest = workflows_dir / workflow
            shutil.copy(source, dest)

        rprint(
            "[green]GitHub workflow configurations added successfully[/green]"
        )
    except FileNotFoundError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to add GitHub workflows\n{e}",
                title="GitHub Workflows Not Added",
                border_style="red",
            )
        )

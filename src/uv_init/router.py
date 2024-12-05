import subprocess
import sys
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path

from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Prompt


@dataclass
class CommandDispatcher:
    """Dispatch commands based on argument pattern"""

    args: Namespace
    original_cwd: Path

    def __post_init__(self) -> None:
        self.project_path = self.original_cwd / self.args.project_name

    def check_dir_exists(self) -> None:
        if self.project_path.exists():
            rprint(
                Panel.fit(
                    f"[red]Error:[/red] Cannot create project '[bold]{self.args.project_name}[/bold]'\n"
                    f"Directory already exists at: [blue]{self.original_cwd}[/blue]\n\n"
                    "Try using a different project name or remove the existing directory.",
                    title="Project Creation Failed",
                    border_style="red",
                )
            )
            sys.exit(1)

    def dispatch(self) -> None:
        """Route to appropriate command handler based on argument pattern"""
        flags = self._get_project_flags()
        self._create_project(flags, workspace=self.args.workspace)

    def _get_project_flags(self) -> list[str]:
        """Convert project type to uv flags"""
        match self.args.type:
            case "lib":
                return ["--lib"]
            case "app":
                return ["--app", "--package"]
            case "package":
                return ["--package"]
            case _:
                raise ValueError(f"Unknown project type: {self.args.type}")

    def _create_project(
        self, flags: list[str], workspace: bool = False
    ) -> None:
        """Create a new project with specified flags"""
        project_type = " ".join(flag.strip("-") for flag in flags)
        rprint(
            f"[green]Creating {project_type} project at {self.original_cwd}...[/green]"
        )
        try:
            subprocess.run(
                [
                    "uv",
                    "init",
                    self.args.project_name,
                    *flags,
                    "--python",
                    self.args.python,
                ],
                check=True,
                cwd=self.original_cwd,
            )
            # Create tests directory
            tests_dir = self.project_path / "tests"
            tests_dir.mkdir(exist_ok=True)
            # Create an empty __init__.py in tests directory
            (tests_dir / "__init__.py").touch()

            rprint(
                f"[green]✓[/green] Successfully created {project_type} project '[bold]{self.args.project_name}[/bold]'"
            )

            if workspace:
                self._initialize_workspace()

        except subprocess.CalledProcessError as e:
            rprint(
                Panel.fit(
                    f"[red]Error:[/red] Failed to create {project_type} project\n{e}",
                    title="Project Creation Failed",
                    border_style="red",
                )
            )
            sys.exit(1)

    def _initialize_workspace(self) -> None:
        """Initialize workspace configuration after project creation"""
        packages_path = self.project_path / "packages"
        packages_path.mkdir(exist_ok=True)
        rprint("[green]Initializing workspace...[/green]")
        common_utils = Prompt.ask(
            "Do you want to add common utilities?",
            choices=["y", "n"],
            default="n",
        )

        if common_utils == "y":
            self._add_common_utils()
        other_projects = Prompt.ask(
            "Do you want to add other projects?",
            choices=["y", "n"],
            default="n",
        )
        if other_projects == "y":
            project_name = Prompt.ask("Enter the project-name: ")
            self._add_other_projects(project_name)

    def _add_common_utils(self) -> None:
        """Add common utilities to the workspace"""
        try:
            subprocess.run(
                [
                    "uv",
                    "init",
                    "common-utils",
                    "--lib",
                ],
                check=True,
                cwd=self.project_path / "packages",
            )
            subprocess.run(
                [
                    "uv",
                    "add",
                    "./packages/common-utils",
                    "--editable",
                ],
                check=True,
                cwd=self.project_path,
            )
            rprint("[green]✓[/green] Successfully added common_utils'")
        except subprocess.CalledProcessError as e:
            rprint(
                Panel.fit(
                    f"[red]Error:[/red] Failed to create common_utils\n{e}",
                    title="Common Utils Creation Failed",
                    border_style="red",
                )
            )
            sys.exit(1)

    def _add_other_projects(self, project_name: str) -> None:
        """Add other projects to the workspace"""
        try:
            subprocess.run(
                [
                    "uv",
                    "init",
                    project_name,
                    "--package",
                    "--app",
                ],
                check=True,
                cwd=self.project_path / "packages",
            )
            subprocess.run(
                [
                    "uv",
                    "add",
                    f"./packages/{project_name}",
                    "--editable",
                ],
                check=True,
                cwd=self.project_path,
            )
            rprint(f"[green]✓[/green] Successfully created {project_name}")
        except subprocess.CalledProcessError as e:
            rprint(
                Panel.fit(
                    f"[red]Error:[/red] Failed to create  {project_name}\n{e}",
                    title="Common Utils Creation Failed",
                    border_style="red",
                )
            )
            sys.exit(1)

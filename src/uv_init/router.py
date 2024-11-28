import os
import subprocess
import sys
from argparse import Namespace
from dataclasses import dataclass, field
from pathlib import Path

from rich import print as rprint
from rich.panel import Panel


@dataclass
class CommandDispatcher:
    """Dispatch commands based on argument pattern"""

    args: Namespace
    original_cwd: Path = field(
        default_factory=lambda: Path(
            os.environ.get("UV_ORIGINAL_CWD", os.getcwd())
        )
    )

    def check_dir_exists(self) -> None:
        project_path = self.original_cwd / self.args.project_name
        if project_path.exists():
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
                return ["--app"]
            case "package":
                return ["--package"]
            case "full":
                return ["--package", "--app"]
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
        # Add workspace initialization logic here
        pass

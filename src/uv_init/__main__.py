import os
import shutil
import sys
from argparse import Namespace
from pathlib import Path

from rich import print as rprint
from rich.panel import Panel

from uv_init.cli import parse_args
from uv_init.dev_deps import add_dev_dependencies, parse_dev_configs
from uv_init.exceptions import GitSetupError, UvInitError
from uv_init.parse_docs import parse_docs
from uv_init.router import CommandDispatcher
from uv_init.setup_git_repo import setup_git_repo


def _rollback(project_path: Path) -> None:
    """Remove an incomplete project directory after a failed creation."""
    if project_path.exists():
        shutil.rmtree(project_path)
        rprint(
            "[yellow]Rolled back: removed incomplete project directory[/yellow]"
        )


def initialize_uv_project(args: Namespace) -> None:
    """Initialize a new uv project with two-phase execution.

    Phase 1 (local): scaffolding, deps, configs, templates.
        On failure, rolls back (removes) the project directory.
    Phase 2 (remote): git commit + GitHub repo creation.
        On failure, warns the user but keeps the local project.
    """
    original_cwd = Path(os.environ.get("UV_ORIGINAL_CWD", os.getcwd()))
    dispatcher = CommandDispatcher(args=args, original_cwd=original_cwd)
    dispatcher.check_dir_exists()

    try:
        # Phase 1: Local project creation (rollback on failure)
        dispatcher.dispatch()
        add_dev_dependencies(args.project_name, dispatcher.project_path)
        parse_dev_configs(dispatcher.project_path)
        parse_docs(args, dispatcher.project_path)
    except UvInitError as e:
        _rollback(dispatcher.project_path)
        rprint(
            Panel.fit(
                f"[red]Error:[/red] {e}",
                title="Project Creation Failed",
                border_style="red",
            )
        )
        sys.exit(1)

    # Phase 2: Git/GitHub setup (no rollback — project is complete locally)
    if args.github:
        try:
            setup_git_repo(
                args.project_name,
                dispatcher.project_path,
                private=args.private,
            )
        except GitSetupError as e:
            rprint(
                Panel.fit(
                    f"[yellow]Warning:[/yellow] GitHub setup failed: {e}\n\n"
                    f"Your project was created successfully at:\n"
                    f"[blue]{dispatcher.project_path}[/blue]",
                    title="GitHub Setup Failed",
                    border_style="yellow",
                )
            )


def main() -> None:
    args = parse_args()
    if args.config:
        from uv_init.config import save_config

        save_config(name=args.config[0], email=args.config[1])
        return
    initialize_uv_project(args)


if __name__ == "__main__":
    main()

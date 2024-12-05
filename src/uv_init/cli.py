import argparse

from rich import print as rprint
from rich.panel import Panel
from rich.text import Text


class RichArgumentParser(argparse.ArgumentParser):
    def format_help(self) -> Panel:
        help_text = Text()

        # Program description
        help_text.append("\nDescription:\n", style="bold cyan")
        help_text.append(f"  {self.description}\n\n")

        # Usage
        help_text.append("Usage:\n", style="bold cyan")
        help_text.append(f"  {self.usage}\n\n")

        # Arguments
        help_text.append("Arguments:\n", style="bold cyan")
        help_text.append("  project_name ", style="bold yellow")
        help_text.append(
            "The name of the project (no spaces or under-scores allowed)\n"
        )

        # Options
        help_text.append("\nOptions:\n", style="bold cyan")
        help_text.append("  -t, --type ", style="bold yellow")
        help_text.append("[lib|package|app] ", style="italic green")
        help_text.append("The type of project to create (default: lib)\n")

        help_text.append("  -p, --python ", style="bold yellow")
        help_text.append("[3.13|3.12|3.11|3.10] ", style="italic green")
        help_text.append("The python version to use (default: 3.12)\n")

        help_text.append("  -w, --workspace ", style="bold yellow")
        help_text.append("Create a workspace\n")

        # Epilog
        help_text.append(f"\n{self.epilog}\n", style="bold blue")

        return Panel(help_text, title="UV Init Help", border_style="cyan")

    def print_help(self):
        rprint(self.format_help())
        exit(0)

    def error(self, message):
        error_message = Text()
        error_message.append("Error: ", style="bold red")
        error_message.append(f"{message}\n\n")
        error_message.append("Usage: ", style="bold")
        error_message.append(self.usage or "No usage information available.")

        panel = Panel(
            error_message, title="Command Line Error", border_style="red"
        )
        rprint(panel)
        exit(2)


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments"""
    parser = RichArgumentParser(
        prog="uv_init",
        description="Initialize a new project",
        usage=(
            "uv_init <project_name> "
            "[-t lib|package|app] "
            "[-p 3.13|3.12|3.11|3.10] "
            "[-w]"
        ),
        epilog="Thanks for using uv_init!",
    )

    parser.add_argument(
        "project_name",
        help="The name of the project (no spaces or under-scores allowed)",
        type=validate_project_name,
    )

    parser.add_argument(
        "-t",
        "--type",
        help="The type of project to create (lib, package, app)",
        default="lib",
        choices=["lib", "package", "app"],
    )

    parser.add_argument(
        "-p",
        "--python",
        help="The python version to use",
        default="3.12",
        choices=["3.13", "3.12", "3.11", "3.10"],
    )

    parser.add_argument(
        "-w",
        "--workspace",
        help="Create a workspace",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-g",
        "--github",
        help="Create a GitHub repository",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def validate_project_name(name: str) -> str:
    if " " in name or "_" in name:
        raise argparse.ArgumentTypeError(
            "Project name cannot contain spaces or under-scores"
        )
    return name



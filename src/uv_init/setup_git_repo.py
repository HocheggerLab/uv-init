import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel


def setup_git_repo(
    project_name: str,
    project_path: Path,
    private: bool = False,  # Added parameter
) -> None:
    """Initialize git repo and optionally set up GitHub remote"""
    # Load environment variables
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = project_name
    try:
        # Create initial commit
        subprocess.run(
            ["git", "add", "."],
            check=True,
            cwd=project_path,
        )
        subprocess.run(
            ["git", "commit", "-m", "feat: initial commit"],
            check=True,
            cwd=project_path,
        )

        if github_token and repo_name:
            # Create GitHub repository
            visibility = "--private" if private else "--public"
            create_repo_cmd = [
                "gh",
                "repo",
                "create",
                repo_name,
                visibility,
                "--source",
                ".",
                "--remote",
                "origin",
                "--push",
            ]

            # Set GitHub token in environment
            env = {
                **dict(os.environ),
                "GITHUB_TOKEN": github_token,
            }

            subprocess.run(
                create_repo_cmd,
                check=True,
                cwd=project_path,
                env=env,
            )

            rprint(
                f"[green]GitHub repository {repo_name} created and configured successfully[/green]"
            )
        else:
            rprint(
                "[yellow]Skipping GitHub setup - no token provided[/yellow]"
            )

    except subprocess.CalledProcessError as e:
        rprint(
            Panel.fit(
                f"[red]Error:[/red] Failed to set up git repository\n{e}",
                title="Git Setup Failed",
                border_style="red",
            )
        )
        exit(1)

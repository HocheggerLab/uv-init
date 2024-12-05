
from argparse import Namespace

from uv_init.cli import parse_args
from uv_init.dev_deps import add_dev_dependencies, parse_dev_configs
from uv_init.parse_docs import parse_docs
from uv_init.router import CommandDispatcher
from uv_init.setup_git_repo import setup_git_repo


def initialize_uv_project(args: Namespace) -> None:
    dispatcher = CommandDispatcher(args)
    dispatcher.check_dir_exists()
    dispatcher.dispatch()
    if args.github:
        setup_git_repo(args.project_name, dispatcher.project_path)
    add_dev_dependencies(args.project_name, dispatcher.project_path)
    parse_dev_configs(dispatcher.project_path)
    parse_docs(args, dispatcher.project_path)

def main() -> None:
    args = parse_args()
    initialize_uv_project(args)


if __name__ == "__main__":
    main()



from uv_init.cli import parse_args
from uv_init.router import CommandDispatcher


def main() -> None:
    args = parse_args()
    dispatcher = CommandDispatcher(args)
    dispatcher.check_dir_exists()
    dispatcher.dispatch()


if __name__ == "__main__":
    main()

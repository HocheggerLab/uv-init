

from uv_init.cli import parse_args
from uv_init.router import initialize_uv_project


def main() -> None:
    args = parse_args()
    initialize_uv_project(args)


if __name__ == "__main__":
    main()

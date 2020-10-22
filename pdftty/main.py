import sys

from .controller import Controller


def main() -> None:
    fname = sys.argv[1]
    Controller(fname).main()


if __name__ == '__main__':
    main()

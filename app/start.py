"""Starts StateSync utility."""

import sys
from view import ConsoleView as Console
from controllers import StateSyncController as State


def main():
    """Starts synchronization."""

    # Checks whether a file path is specified.
    if len(sys.argv) < 2:
        Console().log(
            level="error",
            message="Please, set a path to config file."
        )
        sys.exit(1)

    # Creates instance of App controller.
    state = State()

    # Starts synchronization with OS.
    state.sync_from(filepath=sys.argv[1])
    sys.exit(0)


if __name__ == "__main__":
    main()

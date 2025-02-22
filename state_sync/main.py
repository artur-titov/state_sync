"""Starts StateSync utility."""

import sys
from pathlib import Path

from controllers import StateSync as State
from views import ConsoleView as Console


def run():
    """Validates file and run synchronization."""

    # Checks whether a file path is specified.
    if len(sys.argv) != 2:
        Console().log(
            level="error",
            message="Please, set file path correctly."
        )
        sys.exit(1)

    # Checks if the file exists and is a file.
    if not Path(sys.argv[1]).is_file():
        Console().log(
            level="error",
            message="It seems like file not exists. Please, set correct file path."
        )
        sys.exit(1)

    # Checks whether the config file is supported.
    if Path(sys.argv[1]).suffix not in {".yml", ".yaml"}:
        Console().log(
            level="error",
            message="Sorry, but file with this extension is not supported."
        )
        sys.exit(1)

    # Starts synchronization with OS.
    state = State()
    state.sync_from(filepath=Path(sys.argv[1]))
    sys.exit(0)


if __name__ == "__main__":
    run()

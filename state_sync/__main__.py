"""Starts StateSync utility."""

import sys
from pathlib import Path
from jsonargparse import auto_cli
from dispatcher import Dispatcher as Dispatch
from logs import ConsoleLog as Console


def run(flow: str, config_path: Path):
    """Validates file and run synchronization."""

    # Checks if the file exists and is a file.
    if not Path(config_path).is_file():
        Console().log(
            level="error",
            message="It seems like file not exists. Please, set correct file path."
        )
        sys.exit(1)

    # Checks whether the config file is supported.
    if Path(config_path).suffix not in {".yml", ".yaml"}:
        Console().log(
            level="error",
            message="Sorry, but file with this extension is not supported."
        )
        sys.exit(1)

    Dispatch().now(
        file=Path(config_path),
        arg=flow
    )
    sys.exit(0)


if __name__ == "__main__":
    auto_cli(run)

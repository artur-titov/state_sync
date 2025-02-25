"""Main entrance module."""

import sys

from pathlib import Path
from tools import Parsers, Converters
from services import SyncManager as Sync
from services import StateManager as State
from logs import ConsoleLog as Console


class Dispatcher:
    """Distributes input commands."""

    def __init__(self):
        self._tools = {
            "parser": Parsers,
            "converter": Converters
        }
        self._console = Console()

    def now(self, file: Path, arg: str) -> None:
        """Entrance.

        Parameters
        ----------
        file : str
            Path to config file.
        arg : str
            Target operation (plan, apply)
        """
        # Parse config file.
        parse = self._tools.get("parser")
        try:
            config = parse.yaml(file)
        except IOError as error:
            self._console.log(
                level="error",
                message=error.__cause__
            )
            sys.exit(1)

        # Converts config dict to objects.
        convert = self._tools.get("converter")
        stack = convert.raw_config_to_stack(config)

        # Dispatch
        self._dispatch(stack, arg)

    def _dispatch(self, stack: list[dict], arg: str) -> None:
        """Starts dispatch process.

        Parameters
        ----------
        stack : list[dict]
            Prepared configuration data.
        arg : str
            StateSync case (plan, apply)
        """
        match arg:

            case "plan":
                # Defines state without sync.
                try:
                    State().sync_from(
                        stack=stack,
                        plan_only=True
                    )
                except RuntimeError as error:
                    self._console.log(
                        level="error",
                        message=repr(error)
                    )
                    sys.exit(1)

            case "apply":
                # Begins 'apply' flow.
                try:
                    stack = State().sync_from(
                        stack=stack,
                        plan_only=False
                    )
                    Sync().state_from(stack)
                except RuntimeError as error:
                    self._console.log(
                        level="error",
                        message=repr(error)
                    )
                    sys.exit(1)

            case _:
                self._console.log(
                    level="error",
                    message="Case not supported."
                )
                sys.exit(1)

"""Provides synchronization functionality as a controller."""

import sys
from pathlib import Path

from helpers import yaml_parser as parse
from helpers import raw_config_converter as convert
from services import SyncManager as Sync
from views import ConsoleView as Console


class State:
    """Provides methods for state synchronization as a controller."""

    def __init__(self):
        self._console = Console()

    def sync_from(self, filepath: Path) -> None:
        """Starts synchronization process.

        If the pool is not marked for synchronization it not installs. 
        After that will be print a message.
        If synchronization gets an error, prints result and calls sys.exit(1).
        
        Parameters
        ----------
        filepath : str
            Config file path.
        """
        # Parse config file.
        try:
            configuration = parse(filepath)
        except IOError as error:
            self._console.log(
                level="error",
                message=error.__cause__
            )
            sys.exit(1)

        # Converts items to objects.
        config = convert(configuration)

        # Starts synchronization
        try:
            Sync.state_from(config)
        except (RuntimeError, ValueError) as error:
            self._console.log(
                level="error",
                message=error.__cause__
            )
            sys.exit(1)

    # TODO: get_from(filepath) - like a 'terraform plan'

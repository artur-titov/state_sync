"""Provides synchronization functionality as a controller."""

import sys
from pathlib import Path
from src.helpers.validator import Validator
from src.helpers.printer import Printer as Print
from src.models.parser_model import ParserModel as Parse
from src.models.state_sync_model import StateSyncModel as StateSync


class StateSyncController:
    """Provides methods for state synchronizing as a controller."""


    def check(self, path: Path) -> None:
        """Validates config file before start synchronization.

        If data not valid prints error and calls sys.exit(1).
        
        Parameters
        ----------
        path : Path
            Config file path.
        """
        validate = Validator()

        # Validate file extension
        supported = validate.is_file_supported(path)

        if not supported:
            Print().for_attention(
                "StateSync", 
                "Sorry, but file with this extension is not supported.", 
                "danger"
            )
            sys.exit(1)

        # Check is file exists
        exists = validate.is_file_exists(path)

        if not exists:
            Print().for_attention(
                "StateSync", 
                "Sorry, but it seems the file is not exists.", 
                "danger"
            )
            sys.exit(1)


    def sync_from(self, filepath: Path) -> None:
        """Starts synchronization process.

        If the pool is not marked for synchronization it not installs. 
        After that will be print a message.
        If synchronisation gots an error prints result and calls sys.exit(1).
        
        Parameters
        ----------
        filepath : Path
            Config file path.
        """
        # Parse config file
        config = Parse().yml(filepath)

        # For each pool in installations
        for pool_name in config["global"]["pools_to_synchronize"]:

            # If the pool is not marked for synchronization, we display a message
            if not config["global"]["pools_to_synchronize"][pool_name]:
                Print().for_attention(
                    "StateSyncController",
                    f"'{pool_name}' pool disabled in global settings.",
                    "primary"    
                )

            # If the pool needs to be synchronized, do it
            else:
                # Init syncronizer
                synchronizer = StateSync()

                # Forms the method name as a string
                method_name = f"sync_{pool_name}"
                # Gets the method as an attribute of the object
                method = getattr(synchronizer, method_name)

                # Start synchronization
                try:
                    method(config[pool_name])
                except (RuntimeError, ValueError) as msg:
                    Print().for_attention(
                        "StateSyncController",
                        msg,
                        "danger"
                    )
                    sys.exit(1)

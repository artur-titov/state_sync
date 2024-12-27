"""Starts state-sync utility"""

import sys
from src.helpers.printer import Printer as Print
from src.state_sync_controller import StateSyncController as State


def main():
    """Main function"""

    if len(sys.argv) < 2:
        Print().for_attention("StateSync", "Please, set a config file.", "danger")
        sys.exit(1)

    else:
        config = sys.argv[1]
        state = State()

        # Try to validate file and check is file exists.
        state.check(config)

        # Synchronize config with OS.
        state.sync_from(config)

if __name__ == "__main__":
    main()

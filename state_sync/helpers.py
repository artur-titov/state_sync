"""Provides helpers for StateSync functionality."""

import yaml
import logging

from pathlib import Path
from models import Application, LateCommands


def yaml_parser(filepath: Path) -> dict:
    """Returns as dict all data from parsed YAML file.

    Parameters
    ----------
    filepath : str
        Path to file.

    Returns
    -------
    config : dict
        Configuration file as a Python dictionary.
    """
    try:
        with open(filepath, encoding="utf-8") as config:
            configuration = yaml.safe_load(config)
    except IOError as ioe:
        raise IOError(f"An error occurred while reading the file '{filepath}'.") from ioe

    return configuration


def raw_config_converter(config: dict) -> list:
    """Returns list with objects after dict converting.

    Parameters
    ----------
    config : dict
        Data from parsed YAML file.

    Returns
    -------
    stack : list
        Objects to manipulate.
    """
    stack = []
    models_map = {
        "applications": "Application",
        "late-commands": "LateCommands"
    }

    # From all pools.
    for pool in config["global"]["pool_to_synchronize"]:
        # From all sections in pools.
        for section in config[pool]:
            # Creates stack list.
            pool_model = globals()[models_map[pool]]
            stack.append([
                pool_model.create_from_config(item) for item in config[pool][section]
            ])
    return stack


class ConsoleLogFormatter(logging.Formatter):
    """Logs formatter."""

    def format(self, record):
        """Validates config file before start synchronization.

        If data not valid prints error and calls sys.exit(1).

        Parameters
        ----------
        record : LogRecord
            Log message.

        Returns
        -------
        record : LogRecord
            Returns formatted message.
        """
        marker = {
            "blue": "\033[94m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "red": "\033[91m",
        }
        mark = ""
        clear = "\033[0m"

        if record.levelno == logging.DEBUG:
            mark = marker["blue"]

        if record.levelno == logging.INFO:
            mark = marker["green"]

        if record.levelno == logging.WARNING:
            mark = marker["yellow"]

        if record.levelno == logging.ERROR:
            mark = marker["red"]

        record.name = f"{record.name}:"
        record.levelname = f"{mark}[ {record.levelname} ]{clear}"
        record.msg = f"{mark}{record.msg}{clear}"

        return super().format(record)

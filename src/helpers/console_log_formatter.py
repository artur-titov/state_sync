"""M"""

import logging


class ConsoleLogFormatter(logging.Formatter):
    """D"""

    def format(self, record):
        """D"""
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

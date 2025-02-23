"""Provides console log functionality."""

import logging
from helpers import ConsoleLogFormatter as LogFormat


class ConsoleLog:
    """Provides methods for output logs to console."""

    def __init__(self):
        self.__console_formatter = LogFormat(
            fmt="%(levelname)s %(name)s %(message)s %(asctime)s",
            datefmt="%H:%M:%S"
        )
        self.__console_handler = logging.StreamHandler()
        self.__console_handler.setFormatter(self.__console_formatter)
        self.__logger = logging.getLogger("StateSync")
        self.__logger.setLevel(logging.INFO)
        if not self.__logger.handlers:
            self.__logger.addHandler(self.__console_handler)


    def log(self, level: str, message: str) -> None:
        """Starts logging.
        
        Parameters
        ----------
        level : str
            Log level.
        message: str
            Log message.
        """
        match level:
            case "debug":
                self.__logger.debug(message)
            case "info":
                self.__logger.info(message)
            case "warning":
                self.__logger.warning(message)
            case "error":
                self.__logger.error(message)

"""Provides a class for printing messages in terminal."""

class Printer:
    """Provides a methods for printing messages in terminal."""

    def __init__(self):
        self.__decorate = {
            "disabled": "\033[90m",# grey
            "primary": "\033[94m",# blue
            "success": "\033[32m",# green
            "warning": "\033[33m",# yellow
            "danger": "\033[91m",# red
            "extra": "\033[97;41m",# bg-red
            "bold": "\033[1m",
            "flashing": "\033[5m",
            "underline": "\033[4m",
            "normal": "\033[0m"
        }
        self.__status = {
            "success": "[  OK  ]",
            "failed": "[FAILED]",
            "neutral": "[------]"
        }
        self.__separator = "-->"


    def _make_decorated(self, content: str, style: str) -> str:
        """Decorates input data.
        
        Parameters
        ----------
        content : str
            String that need to decorate.
        style : str
            Style from 'self.__decorate' that will be applying.

        Raises
        ------
        ValueError
            If style not in 'self.__decorate' variable.

        Returns
        -------
        result : str
            Decorated string.
        """
        if style not in self.__decorate:
            raise ValueError(f"Unknown style: {style}")

        result = f"{self.__decorate[style]}{content}{self.__decorate["normal"]}"
        return result


    def _print_result(self, status: str, title: str, description: str) -> None:
        """Prints prepared message in terminal.
        
        Parameters
        ----------
        status : str
            One of the statuses from 'self.__status'
            that will be printed to stdout.
        title : str
            Initiator of the message output
            that will be printed to stdout.
        description : str
            Message body
            that will be printed to stdout.
        """
        print(f"{status} {title} {self.__separator} {description}")


    def to_show_result(self, changed: bool, initiator: str, description: str) -> None:
        """Displays synchronization result.

        If an exception is raised during synchronization, 
        the 'for_attention' method is responsible for decorating it.
        
        Parameters
        ----------
        changed : bool
            Affects the color of the displayed message. 
            If changes have occurred, it will be highlighted 
            in a different color.
        initiator : str
            Initiator of the message output
            that will be printed to stdout.
        description : str
            Message body
            that will be printed to stdout.
        """
        title = self._make_decorated(initiator, "bold")
        status = self._make_decorated(self.__status["success"], "success")

        if changed:
            title = self._make_decorated(title, "warning")
            description = self._make_decorated(description, "warning")

        self._print_result(status, title, description)


    def for_attention(self, initiator: str, msg: str, attention_level: str) -> None:
        """Displays error messages.

        For displaying synchronization result 
        will be better use 'to_show_result' method.
        
        Parameters
        ----------
        initiator : str
            Initiator of the message output
            that will be printed to stdout.
        msg : str
            Message body
            that will be printed to stdout.
        attention_level : str
            Style from 'self.__decorate' that will be applying.
        """
        status = self._make_decorated(self.__status["neutral"], attention_level)
        title = self._make_decorated(initiator, "bold")
        title = self._make_decorated(title, attention_level)
        description = self._make_decorated(msg, attention_level)

        self._print_result(status, title, description)

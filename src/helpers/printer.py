"""Module providing a class for printing messages in terminal."""

class Printer:
    """Class providing a methods for printing in terminal."""

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
        """Input data decoration method"""
        if style not in self.__decorate:
            raise ValueError(f"Unknown style: {style}")

        result = f"{self.__decorate[style]}{content}{self.__decorate["normal"]}"
        return result


    def _print_result(self, state: str, title: str, description: str) -> None:
        """Method description"""
        print(f"{state} {title} {self.__separator} {description}")


    def to_show_result(self, changed: bool, initiator: str, description: str) -> None:
        """Method description"""
        title = self._make_decorated(initiator, "bold")
        state = self._make_decorated(self.__status["success"], "success")

        if changed:
            title = self._make_decorated(title, "warning")
            description = self._make_decorated(description, "warning")

        self._print_result(state, title, description)


    def for_attention(self, initiator: str, msg: str, attention_level: str) -> str:
        """Method description"""
        state = self._make_decorated(self.__status["neutral"], attention_level)
        title = self._make_decorated(initiator, "bold")
        title = self._make_decorated(title, attention_level)
        description = self._make_decorated(msg, attention_level)

        self._print_result(state, title, description)

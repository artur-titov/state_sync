"""Provides model classes."""


class Application:
    """Application model."""

    def __init__(self, data: dict):
        self._name: str = data.get("app")
        self._distributor: str = data.get("distributor")
        self._classic: bool = data.get("classic")

        self._packages: dict = {}
        for package in data["packages"]:
            self._packages[package] = "not_defined"

        # self._commands: list[str]
        self._presented: bool = data.get("presented")

    @classmethod
    def create_from_config(cls, data: dict):
        """Creates Application unit from dict."""
        return cls(data)

    def get_name(self) -> str:
        """Returns unit name."""
        return self._name

    def get_distributor(self) -> str:
        """Returns distributor name."""
        return self._distributor

    def get_items(self) -> dict:
        """Returns unit items."""
        return self._packages

    def set_package_update_case(self, target: str, case: str) -> bool:
        """Sets item updating case."""
        try:
            self._packages.update({target: case})
        except:
            return False
        return True

    def is_classic(self) -> bool:
        """Returns --classic status."""
        return self._classic

    def is_need_to_be_presented(self) -> bool:
        """Returns the desired status of a unit."""
        return self._presented


class LateCommands:
    """Late commands model."""

    def __init__(self, data: dict):
        self._name: str = data.get("group")
        self._commands: str = data.get("commands")
        self._execute: bool = data.get("execute")

    @classmethod
    def create_from_config(cls, data: dict):
        """Creates LateCommands unit from dict."""
        return cls(data)

    def get_name(self) -> str:
        """Returns unit name."""
        return self._name

    def get_items(self) -> str:
        """Returns unit items."""
        return self._commands

    def is_need_to_be_executed(self) -> bool:
        """Returns the desired status of a unit."""
        return self._execute

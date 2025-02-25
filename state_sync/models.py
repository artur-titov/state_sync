"""Module"""


class Application:
    """Class docstring."""

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
        """Creates object Application from dict."""
        return cls(data)

    def get_name(self) -> str:
        """Returns Application name."""
        return self._name

    def get_distributor(self) -> str:
        """Returns distributor name."""
        return self._distributor

    def is_classic(self) -> bool:
        """Returns --classic status."""
        if self.is_classic() is None:
            return False
        return self._classic

    def get_items(self) -> dict:
        """Docstring."""
        return self._packages

    def get_item(self, package: str) -> str:
        """Returns update case."""
        return self._packages[package]

    def set_package_update_case(self, target: str, case: str) -> bool:
        """Sets package update case."""
        try:
            self._packages.update({target: case})
        except:
            return False
        return True

    def is_need_to_be_presented(self) -> bool:
        """Returns the desired status of a Unit."""
        return self._presented


class LateCommands:
    """Class docstring."""

    def __init__(self, data: dict):
        self._name: str = data.get("group")
        self._commands: str = data.get("commands")
        self._execute: bool = data.get("execute")

    @classmethod
    def create_from_config(cls, data: dict):
        """Creates object LateCommands from dict."""
        return cls(data)

    def get_name(self) -> str:
        """Returns Application name."""
        return self._name

    def get_items(self) -> str:
        """Docstring."""
        return self._commands

    def is_need_to_be_executed(self) -> bool:
        """Returns the desired status of a Unit."""
        return self._execute

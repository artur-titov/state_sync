"""Provides model classes."""

from dataclasses import dataclass, field


@dataclass()
class Application:
    """Application model."""
    classic: bool
    presented: bool
    name: str = None
    distributor: str = None
    packages: dict[str, str] = field(default_factory=dict)

    @classmethod
    def create_from_config(cls, data: dict):
        unit = cls(
            name=data.get("app"),
            distributor=data.get("distributor"),
            classic=data.get("classic"),
            presented=data.get("presented")
        )

        for package in data.get("packages", []):
            unit.packages[package] = "not_defined"

        return unit

    def set_package_updating_case(self, target: str, case: str) -> None:
        """Sets item updating case."""
        self.packages.update({target: case})


@dataclass()
class LateCommands:
    """Late commands model."""
    execute: bool
    name: str = None
    commands: list[str] = field(default_factory=list)

    @classmethod
    def create_from_config(cls, data: dict):
        unit = cls(
            name=data.get("group"),
            execute=data.get("execute")
        )

        for command in data.get("commands", []):
            unit.commands.append(command)

        return unit

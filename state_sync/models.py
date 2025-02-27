"""Provides model classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass()
class AbstractUnit(ABC):
    name: str = None
    items: dict[str, str] = field(default_factory=dict)
    additionally: dict[str, any] = field(default_factory=dict)

    @classmethod
    @abstractmethod
    def create_from_config(cls, data: dict) -> 'AbstractUnit':
        pass


@dataclass()
class Application(AbstractUnit):
    """Application model."""

    @classmethod
    def create_from_config(cls, data: dict) -> 'Application':
        """Docstring."""
        unit = cls(name=data.get("app"))

        unit.additionally.update({"classic": data.get("classic")}),
        unit.additionally.update({"distributor": data.get("distributor")}),
        unit.additionally.update({"presented": data.get("presented")}),

        for package in data.get("packages", []):
            unit.items.update({package: "not_defined"})

        return unit

    def set_item_sync_case(self, item: str, case: str) -> None:
        """Sets item updating case."""
        self.items.update({item: case})


@dataclass()
class Command(AbstractUnit):
    """Command unit model."""

    @classmethod
    def create_from_config(cls, data: dict) -> 'Command':
        """Docstring."""
        unit = cls(name=data.get("group"))

        unit.additionally.update({"execute": data.get("execute")})

        for command in data.get("commands", []):
            unit.items.update({command: "as_unit"})

        return unit

"""Module."""

import subprocess

from logs import ConsoleLog as Console
from models import Application, LateCommands


class StateManager:
    """Class docstring."""

    def __init__(self):
        self._run = CommandRunner()
        self._console = Console()

    def sync_from(self, stack: list[dict], plan_only: bool) -> list[dict]:
        """Docstring."""
        for pool in stack:

            # Defines application packages updating case.
            if pool.get("name") == "applications":
                for unit in pool["units"]:
                    packages = unit.get_packages()

                    for package in packages:
                        presented = self._run.package_installation_check(
                            distributor=unit.get_distributor(),
                            package=package
                        )
                        needs_to_be_presented = unit.is_need_to_be_presented()

                        if not presented and needs_to_be_presented:

                            if plan_only:
                                self._console.log(
                                    level="warning",
                                    message=f"{unit.get_name()} ({package}) - will be installed."
                                )
                            else:
                                unit.set_package_update_case(
                                    target=package,
                                    case="to_install"
                                )

                        elif not needs_to_be_presented and presented:

                            if plan_only:
                                self._console.log(
                                    level="warning",
                                    message=f"{unit.get_name()} ({package}) - will be removed."
                                )
                            else:
                                unit.set_package_update_case(
                                    target=package,
                                    case="to_remove"
                                )

                        else:

                            if plan_only:
                                self._console.log(
                                    level="info",
                                    message=f"{unit.get_name()} ({package}) - no needs to be updated."
                                )
                            else:
                                unit.set_package_update_case(
                                    target=package,
                                    case="ignore"
                                )

        return stack


class SyncManager:
    """Class docstring."""

    def __init__(self):
        self._run = CommandRunner()
        self._console = Console()

    def state_from(self, stack: list[dict]):
        """Docstring."""


class CommandRunner:
    """Class docstring."""

    def __init__(self):
        self._installation_command = {
            "apt": "apt install",
            "flatpak": "flatpak install flathub",
            "snap": "snap install",
        }
        self._check_installation = {
            "apt": "dpkg -l | grep",
            "snap": "snap list",
            "flatpak": "flatpak list | grep"
        }

    def package_installation_check(self, distributor: str, package: str) -> bool:
        """Checks if a package is installed on the system.

        Parameters
        ----------
        distributor : str
            Package distributor (apt, snap, etc.).
        package: str
            Item for checking.

        Returns
        -------
        result : bool
            Is package present in OS.
        """
        result = subprocess.run(
            args=f"{self._check_installation[distributor]} {package} > /dev/null 2>&1",
            shell=True,
            check=False
        )
        # if not present
        if result.returncode != 0:
            return False
        # if present
        return True

    @staticmethod
    def unit_install() -> bool:
        """Docstring."""
        return True

    @staticmethod
    def unit_remove() -> bool:
        """Docstring."""
        return True

    @staticmethod
    def late_command() -> bool:
        """Docstring."""
        return True

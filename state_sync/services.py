"""Module with core StateSync functionality."""

import subprocess

from logs import ConsoleLog as Console
from models import Application, LateCommands


class StateManager:
    """Defines the stack state without synchronization."""

    def __init__(self):
        self._run = CommandRunner()
        self._console = Console()

    def sync_from(self, stack: list[dict], plan_only: bool) -> list[dict]:
        """Defines unit item synchronization case.

        Parameters
        ----------
        stack: list[dict]
            Stack of all pools.
        plan_only: bool
            'True' for console output only.
            'False' for pre sync checking where sets update case.

        Returns
        ----------
        list[dict]
            Returns updated stack if 'plan_only' is 'False'.

        Raises
        ----------
        RuntimeError
            From applications: When distributor failure.
        """
        for pool in stack:

            if pool["name"] == "applications":
                for unit in pool["units"]:
                    # Creates Unit context for self._run.app_unit_install().
                    unit_context = {
                        "package": "",
                        "distributor": unit.get_distributor()
                    }
                    # Gets packages for iteration.
                    packages = unit.get_items()

                    for package in packages:
                        unit_context.update({"package": package})

                        # Gets desired unit state.
                        needs_to_be_presented = unit.is_need_to_be_presented()
                        # Gets actual unit state.
                        try:
                            presented = self._run.app_item_installation_check(unit_context)
                        except RuntimeError as exc:
                            raise RuntimeError from exc

                        if not presented and needs_to_be_presented:
                            message = f"{unit.get_name()} ({package}) --> will be installed."
                            case = "to_install"
                            level = "warning"

                        elif not needs_to_be_presented and presented:
                            message = f"{unit.get_name()} ({package}) --> will be removed."
                            case = "to_remove"
                            level = "warning"

                        else:
                            message = f"{unit.get_name()} ({package}) --> no needs to be updated."
                            case = "ignore"
                            level = "info"

                        if plan_only:
                            self._console.log(
                                level=level,
                                message=message
                            )
                        else:
                            unit.set_package_update_case(
                                target=package,
                                case=case
                            )

        return stack


class SyncManager:
    """Manages stack synchronization with OS."""

    def __init__(self):
        self._run = CommandRunner()
        self._console = Console()

    def state_from(self, stack: list[dict]) -> None:
        """Manages synchronization flows based on update case.

        Parameters
        ----------
        stack: list[dict]
            Stack of all pools.

        Raises
        ----------
        RuntimeError
            From Application: When distributor failure or command executed wit error.
            From LateCommands: When ...
        """
        for pool in stack:
            for unit in pool["units"]:

                if isinstance(unit, Application):
                    # Creates Unit context for self._run.app_unit_install().
                    unit_context = {
                        "package": "",
                        "distributor": unit.get_distributor(),
                        "classic": unit.is_classic()
                    }
                    # Gets packages for iteration.
                    packages = unit.get_items()

                    for package, update_case in packages.items():
                        unit_context.update({"package": package})

                        match update_case:
                            case "to_install":
                                self._console.log(
                                    level="warning",
                                    message=f"{unit.get_name()} ({package}) --> Package will be installed."
                                )
                                try:
                                    self._run.app_item_install(
                                        context=unit_context
                                    )
                                except RuntimeError as exc:
                                    raise RuntimeError from exc
                            case "to_remove":
                                self._console.log(
                                    level="warning",
                                    message=f"{unit.get_name()} ({package}) --> Package will be removed."
                                )
                                try:
                                    self._run.app_item_remove(
                                        context=unit_context
                                    )
                                except RuntimeError as exc:
                                    raise RuntimeError from exc

                if isinstance(unit, LateCommands):
                    print(f"LateCommands Unit: {unit.get_name()}")

        self._console.log(
            level="info",
            message="DONE"
        )


class CommandRunner:
    """Defines and execute commands."""

    def __init__(self):
        self._map = {
            "apt": {
                "check": "dpkg -l | grep",
                "install": "apt install"
            },
            "snap": {
                "check": "snap list",
                "install": "snap install"
            },
            "flatpak": {
                "check": "flatpak list | grep",
                "install": "flatpak install flathub"
            }
        }

    @staticmethod
    def _execute(item: str, commands: list[str]) -> bool:
        """Execute shell commands.

        Parameters
        ----------
        item: str
            The name of the item on which the operation is performed.
        commands: list[str]
            List of commands that will be executed.

        Returns
        ----------
        bool
            Returns result (is command executed successfully or not).

        Raises
        ----------
        RuntimeError
            When command executed wit error.
        """
        for command in commands:
            process = subprocess.run(
                args=command,
                shell=True,
                check=False
            )
            if process.returncode != 0:
                raise RuntimeError(f"{item} --> Error code: '{process.returncode}' ({process.stderr})")
        return True

    def app_item_installation_check(self, context: dict) -> bool:
        """Checks if a package is installed on the system.

        Parameters
        ----------
        context : dict
            Unit context.

        Returns
        -------
        bool
            Is package present in OS or not.

        Raises
        ----------
        RuntimeError
            When distributor failure.
        """
        if context["distributor"] not in self._map:
            raise RuntimeError(
                f"{context.get("package")} --> Distributor '{context.get("distributor")}' not supported yet."
            )

        command_to_execute = [
            f"{self._map[context["distributor"]]["check"]} {context["package"]} > /dev/null 2>&1"
        ]
        process = subprocess.run(
            args=command_to_execute,
            shell=True,
            check=False
        )
        if process.returncode != 0:
            return False
        return True

    def app_item_install(self, context: dict) -> bool:
        """Prepares commands for Application unit installation
        and transmit it to execute method.

        Parameters
        ----------
        context : dict
            Unit context.

        Returns
        -------
        bool
            Is installation command executed successfully or not.

        Raises
        ----------
        RuntimeError
            When distributor failure or command executed wit error
        """
        commands_to_execute = []

        match context.get("distributor"):
            case "apt":
                commands_to_execute.append(
                    f"sudo {self._map["apt"]["install"]} {context.get("package")} -y"
                )
            case "flatpak":
                commands_to_execute.append(
                    f"sudo {self._map["flatpak"]["install"]} {context.get("package")} -y"
                )
            case "snap":
                command = f"sudo {self._map["snap"]["install"]} {context.get("package")}"
                if context.get("classic"):
                    command += " --classic"
                commands_to_execute.append(command)
            case _:
                raise RuntimeError(
                    f"{context.get("package")} --> Distributor '{context.get("distributor")}' not supported yet."
                )

        try:
            self._execute(
                item=context.get("package"),
                commands=commands_to_execute
            )
        except RuntimeError as exc:
            raise RuntimeError from exc
        return True

    def app_item_remove(self, context: dict) -> bool:
        """Prepares commands for Application unit removing
        and transmit it to execute method.

        Parameters
        ----------
        context : dict
            Unit context.

        Returns
        ----------
        bool
            Is command executed successfully or not.

        Raises
        ----------
        RuntimeError
            When distributor failure or command executed wit error.
        """
        commands_to_execute = []

        match context.get("distributor"):
            case "apt":
                commands_to_execute.append(
                    f"sudo apt purge {context.get("package")} -y"
                )
                commands_to_execute.append(
                    "sudo apt autoremove -y"
                )
            case "flatpak":
                commands_to_execute.append(
                    f"sudo flatpak kill {context.get("package")}"
                )
                commands_to_execute.append(
                    f"sudo flatpak uninstall -v -y --force-remove --delete-data flathub {context.get("package")}"
                )
                commands_to_execute.append(
                    "sudo flatpak uninstall -y --unused"
                )
            case "snap":
                commands_to_execute.append(
                    f"sudo snap remove --purge {context.get("package")}"
                )
            case _:
                raise RuntimeError(
                    f"{context.get("package")} --> Distributor '{context.get("distributor")}' not supported yet."
                )

        try:
            self._execute(
                item=context.get("package"),
                commands=commands_to_execute
            )
        except RuntimeError as exc:
            raise RuntimeError from exc
        return True

    # def late_command() -> bool:
    #     """Docstring."""
    #     return True

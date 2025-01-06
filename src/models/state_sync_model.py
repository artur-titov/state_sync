"""Provides synchronization functionality."""

import subprocess
from src.helpers.validator import Validator as Validate
from src.helpers.printer import Printer as Print


class StateSyncModel:
    """Provides methods for state synchronizing."""

    def __init__(self):
        self.__installation_command = {
            "apt": "apt install",
            "flatpak": "flatpak install flathub",
            "snap": "snap install",
        }


    def sync_stack(self, pool: dict) -> None:
        """Starts state synchronization.
        
        Defines update case and try it.
        Prints the result after each attempt.
        If something goes wrong, raises an error.

        Parameters
        ----------
        pool : dict
            Pool of items to synchronize.

        Raise
        -------
        RuntimeError
            Re-raise exception to controller.
        """
        for section in pool:
            for app in pool[section]:
                for package in app["packages"]:

                    # Define classic parameter (only for snaps)
                    try:
                        app["classic"]
                        classic = True
                    except Exception:
                        classic = False

                    # Define current package state in OS
                    current_state = Validate().is_package_present(
                        package,
                        app["distributor"]
                    )

                    # Define update case
                    update_case = self._define_update_case(
                        current_state,
                        app["present"]
                    )

                    match update_case:

                        case "install":
                            try:
                                self._install_package(app["distributor"], package, classic)
                                Print().to_show_result(True, package, "Package installed.")
                            except RuntimeError as exc:
                                raise RuntimeError from exc

                        case "remove":
                            try:
                                self._remove_package(app["distributor"], package)
                                Print().to_show_result(True, package, "Package removed.")
                            except RuntimeError as exc:
                                raise RuntimeError from exc

                        case "no_changes":
                            Print().to_show_result(False, package, "No need to update.")


    def _define_update_case(self, present: bool, need_to_present: bool) -> str:
        """Defines update case.
        
        Parameters
        ----------
        present : bool
            Is a package present in OS now.
        need_to_present: bool
            Is a package needs to be present in OS.

        Returns
        -------
        bool : bool
            Returns the update case.
        """
        if not(present) and need_to_present:
            return 'install'

        if not(need_to_present) and present:
            return 'remove'

        return "no_changes"


    def _check_result(self, package: str, return_code: int) -> None | RuntimeError:
        """Raises an exception if the result is bad.
        
        Parameters
        ----------
        package : str
            The package that the data belongs to.
        return_code : int
            Operation exit code.

        Raise
        -------
        RuntimeError
            The method initiator indicated an error when completing the operation.
        """
        if return_code != 0:
            raise RuntimeError(
                f"'{package}' installation return code {return_code} when try to sync stack."
            )


    def _install_package(self, distributor: str, package: str, classic: bool) -> None:
        """Causes the shell command to be run to install the package.

        Runs command and check result after that.
        
        Parameters
        ----------
        distributor : str
            Package distributor (apt, snap, flatpak, etc.).
        package : str
            Package name.
        classic : bool
            Only for snaps with '--classic' argument.
        """
        match distributor:

            case "apt" | "flatpak":
                process = subprocess.run(
                    [f"sudo {self.__installation_command[distributor]} {package} -y"],
                    shell=True,
                    check=False
                )
                self._check_result(package, process.returncode)

            case "snap":
                full_command = f"sudo {self.__installation_command[distributor]} {package}"

                if classic:
                    full_command = f"sudo {self.__installation_command[distributor]} {package} --classic"

                process = subprocess.run(
                    [full_command],
                    shell=True,
                    check=False
                )
                self._check_result(package, process.returncode)


    def _remove_package(self, distributor: str, package: str) -> None:
        """Causes the shell command to be run to remove the package.

        Runs command and check result after that.
        
        Parameters
        ----------
        distributor : str
            Package distributor (apt, snap, flatpak, etc.).
        package : str
            Package name.
        """
        match distributor:
            case "apt":
                process = subprocess.run([f"sudo apt purge {package} -y"], shell=True, check=False)
                self._check_result(package, process.returncode)

                process = subprocess.run(["sudo apt autoremove -y"], shell=True, check=False)
                self._check_result(package, process.returncode)

            case "flatpak":
                process = subprocess.run([f"sudo flatpak kill {package}"], shell=True, check=False)
                self._check_result(package, process.returncode)

                process = subprocess.run([
                    f"sudo \
                    flatpak \
                    uninstall \
                    -v \
                    -y \
                    --force-remove \
                    --delete-data \
                    flathub \
                    {package}"
                ], shell=True, check=False)
                self._check_result(package, process.returncode)

                process = subprocess.run([
                    "sudo flatpak uninstall -y --unused"
                ], shell=True, check=False)
                self._check_result(package, process.returncode)

            case "snap":
                process = subprocess.run([
                    f"sudo snap remove --purge {package}"
                ], shell=True, check=False)
                self._check_result(package, process.returncode)

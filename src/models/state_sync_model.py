"""Module description"""

import subprocess
from src.helpers.validator import Validator as Validate
from src.helpers.printer import Printer as Print


class StateSyncModel:
    """Class description"""

    def __init__(self):
        self.validate = Validate()
        self.__installation_command = {
            "apt": "apt install",
            "flatpak": "flatpak install flathub",
            "snap": "snap install",
        }


    def sync_stack(self, pool: dict) -> None:
        """Method description"""

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
                    current_state = self.validate.is_package_present(
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
        """Method description"""

        if not(present) and need_to_present:
            return 'install'

        if not(need_to_present) and present:
            return 'remove'

        return "no_changes"


    def _check_result(self, package: str, return_code: int) -> None | RuntimeError:
        """Method description"""
        if return_code != 0:
            raise RuntimeError(
                f"{package} return code { return_code } when try to sync stack."
            )


    def _install_package(self, distributor: str, package: str, classic: bool) -> None | RuntimeError:
        """Method description"""

        match distributor:

            case "apt" | "flatpak":
                process = subprocess.run(
                    [f"sudo {self.__installation_command[distributor]} {package} -y"],
                    shell=True,
                    check=False
                )
                self._check_result(package, process.returncode)

            case "snap":
                if classic:
                    process = subprocess.run(
                        [f"sudo {self.__installation_command[distributor]} {package} --classic"],
                        shell=True,
                        check=False
                    )
                    self._check_result(package, process.returncode)

                process = subprocess.run(
                    [f"sudo {self.__installation_command[distributor]} {package}"],
                    shell=True,
                    check=False
                )
                self._check_result(package, process.returncode)


    def _remove_package(self, distributor: str, package: str) -> None:
        """Method description"""

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
                    "sudo flatpak uninstall --unused"
                ], shell=True, check=False)
                self._check_result(package, process.returncode)

            case "snap":
                process = subprocess.run([
                    f"sudo snap remove --purge {package}"
                ], shell=True, check=False)
                self._check_result(package, process.returncode)

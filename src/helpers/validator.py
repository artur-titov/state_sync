"""Module description"""

import re
import subprocess
from pathlib import Path


class Validator:
    """Class description"""

    def __init__(self):
        self.__installation_check = {
            "apt": "dpkg -l | grep",
            "snap": "snap list",
            "flatpak": "flatpak list | grep"
        }


    def is_file_supported(self, path: Path) -> bool:
        """Method description"""
        supported = re.compile(r".*\.(yml|yaml)$", re.I)
        return bool(supported.match(path))


    def is_file_exists(self, filepath: Path) -> bool:
        """Method description"""
        path = Path(filepath)
        exists = path.is_file()

        if not exists:
            return False

        return True


    def is_package_present(self, package: str, distributor: str) -> bool:
        """Method description"""
        process = subprocess.run(
            f"{self.__installation_check[distributor]} {package} > /dev/null 2>&1",
            shell=True,
            check=False
        )

        if process.returncode == 0:
            # if present
            return True

        return False

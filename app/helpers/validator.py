"""Provides validation functionality."""

import re
import subprocess
from pathlib import Path


class Validator:
    """Provides methods for data validation."""

    def __init__(self):
        self.__installation_check = {
            "apt": "dpkg -l | grep",
            "snap": "snap list",
            "flatpak": "flatpak list | grep"
        }


    def is_file_supported(self, file: Path) -> bool:
        """Validates config file extension.
        
        Parameters
        ----------
        file : Path
            Path to file.

        Returns
        -------
        bool : bool
            Supported or not.
        """
        supported = re.compile(r".*\.(yml|yaml)$", re.I)
        return bool(supported.match(file))


    def is_file_exists(self, filepath: Path) -> bool:
        """Checks if file exists.

        Path to remote file is not supported and
        will be interpreted as 'file is not exists'.
        
        Parameters
        ----------
        filepath : Path
            Path to file.

        Returns
        -------
        bool : bool
            Exists or not.
        """
        path = Path(filepath)
        exists = path.is_file()

        if not exists:
            return False

        return True


    def is_package_present(self, package: str, distributor: str) -> bool:
        """Checks if a package is installed on the system.
        
        Parameters
        ----------
        package : str
            Package name.
        distributor : str
            Package distributor (apt, snap, flatpak, etc.)

        Returns
        -------
        bool : bool
            Present or not.
        """
        process = subprocess.run(
            f"{self.__installation_check[distributor]} {package} > /dev/null 2>&1",
            shell=True,
            check=False
        )

        if process.returncode == 0:
            # if present
            return True

        return False

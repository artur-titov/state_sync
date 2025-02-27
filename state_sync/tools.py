"""Tools for Dispatcher."""

from pathlib import Path
import yaml
from models import Application, LateCommands


class Parsers:
    """Defines parsers functionality."""

    @staticmethod
    def yaml(file_path: Path) -> dict:
        """Returns all data from parsed YAML file as a dict.

        Parameters
        ----------
        file_path : str
            Path to file.

        Returns
        -------
        dict
            Configuration file as a Python dictionary.

        Raises
        -------
        RuntimeError
            When error occurred while reading the file.
        """
        try:
            with open(file_path, encoding="utf-8") as config:
                configuration = yaml.safe_load(config)
        except IOError as ioe:
            raise RuntimeError(
                f"An error occurred while reading the file '{file_path}'."
            ) from ioe

        return configuration


class Converters:
    """Defines converters functionality."""

    @staticmethod
    def raw_config_to_stack(config: dict) -> list[dict]:
        """Converts units from configuration
        dictionary to objects.

        Parameters
        ----------
        config : dict
            Data from parsed YAML file.

        Returns
        -------
        list[dict]
            List of dictionaries with objects.

        Raises
        -------
        RuntimeError
            If pool model not supported.
        """
        stack = []
        models_map = {
            "applications": Application,
            "late_commands": LateCommands
        }

        # From all pools.
        for record in config["global"]["pool_to_synchronize"]:

            pool = {
                "name": record,
                "units": []
            }

            # Sets pool Model.
            match record:
                case "applications":
                    pool_model = models_map.get("applications")
                case "late_commands":
                    pool_model = models_map.get("late_commands")
                case _:
                    raise RuntimeError(f"Pool Model for {pool} not supported yet.")

            # From all sections in pool.
            for section in config[record]:

                for unit in config[record][section]:
                    pool["units"].append(
                        pool_model.create_from_config(unit)
                    )

            stack.append(pool)

        return stack

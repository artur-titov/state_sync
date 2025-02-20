"""Provides file parsing functionality."""

from pathlib import Path
import yaml


class ParserModel:
    """Provides methods for file parsing."""

    def yml(self, filepath: Path) -> dict:
        """Translates a YAML file into a Python dictionary.
        
        Parameters
        ----------
        filepath : Path
            Path to file.

        Returns
        -------
        config : dict
            Configuration file as a Python dictionary.
        """
        with open(filepath, encoding="utf-8") as configuration:
            config = yaml.load(configuration, Loader=yaml.SafeLoader)

        return config

"""Module description"""

from pathlib import Path
import yaml


class ParserModel:
    """Class description"""

    def yml(self, filepath: Path) -> dict:
        """Method description"""

        with open(filepath, encoding="utf-8") as configuration:
            config = yaml.load(configuration, Loader=yaml.SafeLoader)

        return config

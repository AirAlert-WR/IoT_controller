from configparser import ConfigParser

class ConfigurationReader:
    """
    Class for loading configuration entries from a file
    """

    def __init__(self, filename: str) -> None:
        """
        Custom constructor for initializing
        :param filename: The path for the file to be loaded
        """
        # Reading into the internal parser
        self._parser = ConfigParser()
        self._parser.read(filename)


    def for_section(self, section: str = "") -> dict[str,str]:
        """
        Method to load the configuration file for the mqtt logic

        :param section: The section inside the config to load

        :returns: A non-empty object containing key-value-pairs
        """
        # Return empty object if section not found
        if section not in self._parser:
            print(f"WARNING: Section '{section}' not found in parser file. Returning empty structure.")
            return {}

        # Return the loaded entries for the section
        return dict(self._parser[section])

import platform
def is_raspberrypi() -> bool:
    return platform.machine().startswith("arm") and "raspberrypi" in platform.uname().node.lower()
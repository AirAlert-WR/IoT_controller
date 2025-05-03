from abc import ABC

class AbstractConfigurable(ABC):
    """
    ABSTRACT: Class for providing a key-value configuration environment
    """

    def __init__(self, config: dict[str,any]) -> None:
        """
        Constructor
        :param config: the config section
        """
        # Filter the config for the own section and pack it
        self._config = self.mod_config(config)

    @classmethod
    def section(cls) -> str:
        """
        :return: the section string for the global key-value configuration
        """
        pass

    @classmethod
    def mod_config(cls, loaded_config: dict[str,any]) -> dict[str,any]:
        """
        Method for replacing values of an input configuration with valid (default) ones
        :param loaded_config: the input dictionary
        :return: a configuration dictionary
        """
        pass

DEF_CONFIG_FILE = "config.ini"
"""
The default path for the program's config file
"""

from configparser import ConfigParser
class GlobalConfiguration:

    def __init__(self, filename: str = DEF_CONFIG_FILE) -> None:
        """
        Custom constructor
        :param filename: path to the configuration file
        """
        # Save the file name
        self._filename = filename
        # Create and load the configuration parser
        self._config_parser = ConfigParser()
        self._config_parser.read(self._filename)

    def for_configurable(self, configurable: type[AbstractConfigurable]) -> dict[str, any]:
        """
        Method for obtaining a configuration dictionary for a specific object
        :param configurable: the type of the configurable object
        :return: NON-EMPTY dictionary
        """
        return dict(self._config_parser[configurable.section()])

    def correct_configuration(self, list_of_configurables: list[type[AbstractConfigurable]]) -> None:
        """
        Method for replacing / completing the loaded configration for configurable objects
        :param list_of_configurables: A list of typed configurable classes to save
        """
        # Do for all given entries
        for configurable in list_of_configurables:
            # Load the current config for the according object
            config = self.for_configurable(configurable)
            # Perform the checking procedure
            self._config_parser[configurable.section()] = configurable.mod_config(config)

    def save(self) -> None:
        """
        Method for saving the configuration entries to the originally loaded file
        """
        with open(self._filename, 'w', encoding="utf-8") as config_file:
            self._config_parser.write(config_file)  # TODO fix warning


import platform
def is_raspberrypi() -> bool:
    """
    :return: state if platform is REALLY an arm-based raspberry pi
    """
    return platform.machine().startswith("arm") and "pi" in platform.uname().node.lower()
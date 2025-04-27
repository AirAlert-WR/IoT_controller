from abc import ABC

class AbstractConfigurable(ABC):
    """
    ABSTRACT: Class for providing a key-value configuration environment
    """

    def __init__(self, global_config: dict[str,any]):
        """
        Constructor
        :param global_config: the global configuration to filter
        """
        # Filter the config for the own section and pack it
        self._config = self.mod_config(global_config.get(self.section(),{}))

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

import platform
def is_raspberrypi() -> bool:
    """
    :return: state if platform is REALLY an arm-based raspberry pi
    """
    return platform.machine().startswith("arm") and "raspberrypi" in platform.uname().node.lower()
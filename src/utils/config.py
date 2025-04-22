from configparser import ConfigParser

def load_config(filename: str, section: str = "default") -> dict[str, str]:
    """
        Method to load the configuration file for the mqtt logic
        :param filename: The name of the file to load
        :param section: The section inside the file to load

        :returns: A not-empty object containing key-value-pairs
    """
    # Reading and parsing the file
    parser = ConfigParser()
    parser.read(filename)

    # Return empty object if section not found
    if section not in parser:
        print(f"WARNING: Section '{section}' not found in parser file. Returning empty structure.")
        return {}

    # Return the loaded entries for the section
    return dict(parser[section])


DEF_CONF_FILE = "config.ini"
"""
    Constant path to the central configuration file
"""
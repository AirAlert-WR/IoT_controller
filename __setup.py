import os

from setuptools import setup

from src.utils import is_raspberrypi

'''
Setup script for installation and default configuration
'''

# Basic requirements
_base_requirements = [
    "paho-mqtt",
]

# Raspberry-Pi-specific requirements
_rpi_requirements = [
    "sds011lib",
    "adafruit-circuitpython-ads1x15",
    "adafruit-blinka",
]

# Getting platform
is_rpi = is_raspberrypi()
# Printing warning if not Raspberry-Pi
if not is_rpi:
    print("WARNING (__setup.py): You are trying to setup on a non-raspberry-pi platform.\n"
          "Therefore, some dependencies will not be installed. Instead, dummy values will be used.")

# Combining requirements
install_requires = _base_requirements + (_rpi_requirements if is_rpi else [])

setup(
    name="AirAlert_IoT-controller",
    version="0.1",
    author= "AirAlert",
    description="IoT-controller software for the AirAlert project",
    install_requires=install_requires,
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

from src.utils import AbstractConfigurable, DEF_CONFIG_FILE
# Load all configurable classes:
from src.mqtt import MQTTManager

configurable_classes: list[type[AbstractConfigurable]] = [
    MQTTManager
]

# Setting all config keys for the mqtt manager
from configparser import ConfigParser
import configparser
cp = ConfigParser()

for configurable in configurable_classes:
    section = configurable.section()
    cp[section] = configurable.mod_config({})

# Writing the file
with open(DEF_CONFIG_FILE, 'w', encoding="utf-8") as config_file:
    cp.write(config_file)

# creating directories
try:
    os.mkdir("certs")
except Exception as e:
    print("Error while creating directory")
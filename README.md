# AirAlert_IoT_Controller
Code for Raspberry Pi to use as the IoT controller for the project "AirAlert"

## Installation and initialization

### Software

Make sure you have the following programs installed on your device:

- Python >= 3.11
- PIP

For example, under a **Debian-based Linux** platform like "*RaspberryPi OS*", these programs may be installed through the following **shell command**:

    sudo apt update && sudo apt install python3 python3-pip

After a successful preparation, simply execute the **following passage** inside your shell, while setting its path to the **current folder**:

    pip install .

This will perform the complete program initialization by:

- installing all dependencies (if available on your platform)
- creating all configuration files with according default entries

### Hardware

> !!! Attention !!!

## Starting the program

### Simple execution

To run this application for a single time, just execute the **following code** in your command line:

    ./main.py

If it shouldn't work, please enable execution privileges for this file, using either **chmod** or some other tool.

### Execution on startup

Normally, this software should operate since the controller operating system has started.
Therefore, a service registration is necessary.

TODO

## Configuration

The central config file, saved under **config.ini**, consists of the following sections

### mqtt

This section stores configuration values for the MQTT manager:

|     key     | description                               |
|:-----------:|:------------------------------------------|
|  username   | the username of the client account        |
|  password   | the password of the client account        |
|     id      | the id of the client account              |
|   ca_root   | path to the root certificate file         |
|   ca_main   | path to the main certificate file         |
| key_private | path to the key file for the certificates |
|    host     | the basic url to the mqtt server          |
|    port     | the port for accessing the mqtt task      |
# AirAlert_IoT_Controller
Code for Raspberry Pi to use as the IoT controller for the project "AirAlert"

## Installation and initialization

Make sure you have the following programs installed on your device:

- Python >= 3.11
- PIP

Simply execute the **following code** in your command line, after setting its path to the current folder:

    pip install .

This will perform the complete program initialization by:

- Installing all dependencies (if available on your platform)
- Creating all configuration files with according default entries

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

The central config file (format: INI) consists of the following sections

### mqtt

This section stores configuration values especially for the MQTT manager:

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
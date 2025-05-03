# AirAlert_IoT_Controller
Code for Raspberry Pi to use as the IoT controller for the project "AirAlert"

## Installation and initialization

### Software

Make sure you have the following programs installed on your device:

- Python >= 3.11
- PIP

For example, under a **Debian-based Linux** platform like "*RaspberryPi OS*", these programs may be installed through the following **shell command**:

    sudo apt update && sudo apt install python3 python3-pip

After a successful installation, proceed at one of the next subsections **according to your case**.

#### 1. ANY platform

Simply execute the **following passage** inside your shell, while setting its path to the **current folder**:

    pip install .

This will install all python-specific requirements.

#### 2. ONLY Raspberry-Pi

If you want to install on a Raspberry-Pi controller (the target platform the whole application INITIALLY is created for), execute the **following line instead**:

    pip install .[rpi]

This will install all dependencies only available for this platform (e.g. some sensor hardware implementations).

### Hardware

> !!! Attention !!!

## Starting the program

### Simple execution

To run this application for a single time, just execute the **following code** in your command line:

    ./main.py

If it shouldn't work, please enable execution privileges for this file, using either **chmod** or some other tool.

### Execution on system boot

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
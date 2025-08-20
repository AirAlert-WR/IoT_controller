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

> !!! Attention !!!
> use the parameter **--break-system-packages**, if necessary

### Hardware

> !!! Attention !!!
> The Controller application **generally runs on every platform** where Python is installed.
> However, the full code is only executed on the Raspberry Pi, as all dependencies can only be installed there.
> Nevertheless, a dummy-mode application will run on any different computer architecture, so connection privileges, mqtt bridges and much more can be tested independently.

## Starting the program

The following steps will be **shown for the Linux** plattform. But on Windows, similar instructions should also work.

### Simple execution

First of all, clone the repository and install the initial exception.

Then, if necessary, obtain a certificate zip, usually possible while registering or having insight into controller properties on the frontend web page:

    wget [ZIP-URL] -O temp.zip && unzip temp.zip && rm temp.zip

To run this application for a single time, just execute the **following code** in your command line:

    ./main.py

If it shouldn't work, please enable execution privileges for this file, using either **chmod** or some other tool.

### Execution on system boot

Normally, this software should operate since the controller operating system has started.
Therefore, a service registration is necessary.

Execute the following code inside the command line:

    sudo nano /etc/systemd/system/iot_controller.service

Add these lines to the newly created text file. **Edit the ExecStart and WorkingDirectory paths, if necessary**

    [Unit]
    Description=AirAlert IoT Controller software
    After=network.target

    [Service]
    ExecStart=python /home/admin/IoT_controller/main.py
    WorkingDirectory=/home/admin/IoT_controller
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=admin

    [Install]
    WantedBy=multi-user.target

Then save the file (CTRL + O) and enable the service:

    chmod +x /home/admin/IoT_controller/main.py
    sudo systemctl enable iot_controller.service
    sudo systemctl start iot_controller.service

Now, the service should not only run, but execute at every startup (exaclty after the network connection is initialized).
For additional checks and insights into log messages and errors, use the following command:

    sudo systemctl status iot_controller.service


## Configuration

The central config file, saved under **config.ini**, consists of the following sections

### mqtt

This section stores configuration values for the MQTT manager:

|     key          | description                               |
|:----------------:|:------------------------------------------|
|  username        | the username of the client account        |
|  password        | the password of the client account        |
|     id           | the id of the controller                  |
| path_rootca      | path to the root certificate file         |
| path_certificate | path to the main certificate file         |
| path_privatekey  | path to the unique key file for the client|
| use_tls          | state wheter certificate- or login-based  |
|    host          | the basic url to the mqtt server          |
|    port          | the port for accessing the mqtt task      |

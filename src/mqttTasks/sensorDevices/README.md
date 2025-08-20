# Sensor information

For gathering data from the surrounding environment, various types of sensors are utilized.

This README provides insight into the sensors used for the *AirAlert* project, 
providing information about their **specification** as well as the **measured data values**

## SDS011

### Information

This sensor is used for getting the **amount of particulate matter** inside the air, such as **PM2.5 and PM10**,
which, at high concentration, could literally provide a "dangerous atmosphere", therefore increasing mortality due to **blockage of the bronchi** and resulting **suffocation**.

The device operates using the optical phenomenon of **particle reflection**, which is then captured by a photo diode.

All raw data is transferred by the **USB2TT converter** provided inside the bought bundle.
The sensor itself is **calibrated from factory**.

The according module for the *AirAlert* project is located under:

    src.mqttTasks.sensorDevices.sds011.SensorSDS011

### Measured data

The following table collects all data values that can be accessed after a single measuring cycle.

> **Attention**: all values are saved as **floating point numbers**

|  Key  | Description                          | Quantity |
|:-----:|:-------------------------------------|:--------:|
| pm2.5 | Amount of PM2.5 particles in the air |  µg/m^3  |
| pm10  | Amount of PM10 particles in the air  |  µg/m^3  |

## SCD41

### Information

This sensor is used for gathering information about the air quality, such as:
- the **amount of carbon dioxide** 
- the environmental **temperature**
- the **relative humidity**

The device operates using TODO

All raw data is (currently) transferred by the Raspberry Pi's ONLY **I2C input** located at the gpio pins.
The sensor itself is **calibrated from factory**.

> **Attention**: the implementation of an **I2C multiplexer** for connecting multiple sensors to the Raspberry Pi 
> **IS NOT THERE**. You will have to rewrite the source code on your own then.

The according module for the *AirAlert* project is located under:

    src.mqttTasks.sensorDevices.sdc41.SensorSCD41

### Measured data

The following table collects all data values that can be accessed after a single measuring cycle.

> **Attention**: all values are saved as **floating point numbers**

|     Key     | Description                             | Quantity  |
|:-----------:|:----------------------------------------|:---------:|
| temperature | Thermal temperature of the environment  |    °C     |
|     co2     | Amount of CO2 molecules in the air      | 1/(10^-6) |
|  humidity   | Amount of Water in the air (Saturation) |  % (rH)   |

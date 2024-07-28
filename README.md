# ESP32 Temperature Sensor

This project is a proof-of-concept (POC) for an IoT course at Aalborg UCN, part of the Software Development program. The goal is to develop a temperature monitoring system using an ESP32 microcontroller, a FireBeetle display, and a menu with input control.

## Features

- Temperature measurement using the ESP32's internal sensor.
- Display temperature data on a 128x64 OLED screen.
- Menu-driven interface for user interaction.
- MQTT communication with Azure IoT Hub.
- Wi-Fi connectivity with a captive portal for easy configuration.

## Hardware Requirements

- [FireBeetle ESP32](https://www.dfrobot.com/product-1590.html)
- [DFRobot OLED Display (128x64)](https://www.dfrobot.com/product-1744.html)

## Software Requirements

- Python 3.x
- MicroPython firmware for ESP32
- `esptool` and `ampy` for flashing and file transfer
- file transfer and flashing can be achieved easily with Thonny IDE or VS Code with the Pymakr extension

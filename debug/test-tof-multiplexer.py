#!/usr/bin/env python3

# sourced from https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/circuitpython-python

# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices
import board
import adafruit_tca9548a
import adafruit_vl53l4cd


# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c, 0x71)

# this is specific to scatbot configuration
# we have 4 vl53L4 sensors in the front bumper
sensor_channels = []
sensors = []


def display_sensor_stats(channel, sensor):
    print("--------------------")
    print(f"VL53L4CD {channel=}.")
    model_id, module_type = sensor.model_info
    print("Model ID: 0x{:0X}".format(model_id))
    print("Module Type: 0x{:0X}".format(module_type))
    print("Timing Budget: {}".format(sensor.timing_budget))
    print("Inter-Measurement: {}".format(sensor.inter_measurement))
    print("--------------------")


for channel in range(8):
    print(f"Channel {channel}:")
    if tca[channel].try_lock():
        addresses = tca[channel].scan()
        for address in addresses:
            if address != 0x71:
                print(hex(address))
            if address == 0x29:
                sensor_channels.append(channel)

        tca[channel].unlock()

for channel in sensor_channels:
    vl53 = adafruit_vl53l4cd.VL53L4CD(tca[channel])
    # OPTIONAL: can set non-default values
    vl53.inter_measurement = 0
    vl53.timing_budget = 200
    vl53.start_ranging()
    sensors.append(vl53)
    display_sensor_stats(channel, vl53)

while True:
    distances = []
    for i in range(len(sensors)):
        sensor = sensors[i]
        channel = sensor_channels[i]

        while not sensor.data_ready:
            pass

        sensor.clear_interrupt()
        distances.append(sensor.distance)

    print(", ".join("{:3.2f}".format(distance) for distance in distances))

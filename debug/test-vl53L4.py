#!/usr/bin/env python3

# Sourced from https://github.com/adafruit/Adafruit_CircuitPython_VL53L4CD/blob/212cdf04e5b70e6ab27931e72215405f2eb765f4/examples/vl53l4cd_simpletest.py

# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of the VL53L4CD distance sensor.
# Will print the sensed range/distance every second.
import time
import board
import adafruit_vl53l4cd

i2c = board.I2C()

vl53 = adafruit_vl53l4cd.VL53L4CD(i2c)

# OPTIONAL: can set non-default values
vl53.inter_measurement = 0
vl53.timing_budget = 200

print("VL53L4CD Simple Test.")
print("--------------------")
model_id, module_type = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Timing Budget: {}".format(vl53.timing_budget))
print("Inter-Measurement: {}".format(vl53.inter_measurement))
print("--------------------")

vl53.start_ranging()
while True:
    t1 = time.time()
    while not vl53.data_ready:
        pass
    vl53.clear_interrupt()
    print(f"Distance: {vl53.distance}cm  time: {time.time() - t1}")

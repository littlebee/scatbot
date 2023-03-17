#!/usr/bin/env python3

# from :
# https://github.com/adafruit/Adafruit_CircuitPython_MotorKit/blob/main/README.rst#usage-example

import time
from adafruit_motorkit import MotorKit

from commons import constants

kit = MotorKit(constants.MOTOR_I2C_ADDRESS)

motors = [kit.motor1, kit.motor2, kit.motor3, kit.motor4]

# 0.1 is not enough to turn the motor, but ...
print("You should hear an audible whine from each motor in succession")

for i, motor in enumerate(motors):
    print(f"testing motor {i}")
    motor.throttle = 0.7
    time.sleep(2)
    motor.throttle = 0

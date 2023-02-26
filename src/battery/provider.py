import os
import time
import json
import asyncio
import traceback
import websockets

from commons import constants, messages

import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

i2c_bus = board.I2C()
ina219 = INA219(i2c_bus)
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V


async def provide_state():
    while True:
        try:
            print(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                await messages.send_identity(websocket, "compass")
                while True:
                    message = json.dumps(
                        {
                            "type": "updateState",
                            "data": {
                                "battery": {
                                    "voltage": ina219.bus_voltage,
                                    "current": ina219.current / 1000,
                                }
                            },
                        }
                    )
                    await websocket.send(message)
                    # print(f"{datetime.datetime.now()}: {message}", flush=True)

                    if ina219.bus_voltage < constants.BATTERY_SHUTDOWN_VOLTAGE:
                        print(
                            f"battery critical @{ina219.bus_voltage}V .  shutting down",
                            flush=True,
                        )
                        os.system("shutdown now")

                    await asyncio.sleep(constants.BATTERY_SAMPLE_INTERVAL)
        except:
            traceback.print_exc()

        print("socket disconnected.  Reconnecting in 5 sec...")
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

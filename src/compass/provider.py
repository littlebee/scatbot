import time
import json
import smbus
import asyncio
import traceback
import websockets

from commons import constants, messages, log

bus = smbus.SMBus(constants.I2C_BUS)


# Make clockwise negative
def get_heading():
    bear1 = bus.read_byte_data(constants.COMPASS_ADDRESS, 2)
    bear2 = bus.read_byte_data(constants.COMPASS_ADDRESS, 3)
    bear = (bear1 << 8) + bear2
    bear = bear / 10.0
    return add_degrees(bear, constants.COMPASS_MAGNETIC_OFFSET)


def add_degrees(heading, deg):
    newHeading = heading + deg
    if newHeading < 0:
        newHeading = 360 - newHeading
    if newHeading > 360:
        newHeading -= 360
    return newHeading


def diff_degrees(deg1, deg2):
    deg1_adj = deg1 + 180 if deg1 < 180 else deg1 - 180
    deg2_adj = deg2 + 180 if deg2 < 180 else deg2 - 180

    return deg1_adj + deg2_adj


async def provide_state():
    sample_count = 0
    last_sample = 0
    while True:
        try:
            log.info(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                await messages.send_identity(websocket, "compass")
                while True:
                    sample = get_heading()
                    diff = abs(sample - last_sample)
                    last_sample = sample
                    if diff > constants.COMPASS_CHANGE_TOLERANCE:
                        message = json.dumps(
                            {
                                "type": "updateState",
                                "data": {"compass": sample},
                            }
                        )
                        await websocket.send(message)
                    sample_count += 1
                    await asyncio.sleep(constants.COMPASS_SAMPLE_INTERVAL)
        except:
            traceback.print_exc()

        log.info("socket disconnected.  Reconnecting in 5 sec...")
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

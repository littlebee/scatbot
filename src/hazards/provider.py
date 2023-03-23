import time
import json
import asyncio
import traceback
import websockets

import board
import adafruit_tca9548a
import adafruit_vl53l4cd

from commons import constants, messages, log

LEFT_FRONT_SENSOR = 0
RIGHT_FRONT_SENSOR = 1
FRONT_SENSOR = 2
FRONT_CLIFF_SENSOR = 3

SENSOR_CHANNELS = [
    4,  # LEFT FRONT
    5,  # RIGHT FRONT
    6,  # CENTER FRONT
    7,  # CENTER FRONT CLIFF
]

HAZARD_TYPE_COLLISION = "collision"
HAZARD_TYPE_CLIFF = "cliff"

SIDE_SENSOR_MIN_DIST = 6
SIDE_SENSOR_MAX_DIST = 15
FRONT_SENSOR_MIN_DIST = 5
FRONT_SENSOR_MAX_DIST = 15


# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c, 0x71)

# this is specific to scatbot configuration
# we have 4 vl53L4 sensors in the front bumper
sensor_channels = []
sensors = []

for channel in SENSOR_CHANNELS:
    vl53 = adafruit_vl53l4cd.VL53L4CD(tca[channel])
    # OPTIONAL: can set non-default values
    vl53.inter_measurement = 0
    vl53.timing_budget = 200
    vl53.start_ranging()
    sensors.append(vl53)


def get_distances():
    distances = []
    for i in range(len(sensors)):
        sensor = sensors[i]

        while not sensor.data_ready:
            pass

        sensor.clear_interrupt()
        distances.append(sensor.distance)

    return distances


def detect_hazards_front(distances):
    hazards = []
    left_front_dist, right_front_dist, front_dist, front_cliff_dist = distances

    if left_front_dist > SIDE_SENSOR_MAX_DIST:
        hazards.append({"sensor": LEFT_FRONT_SENSOR, "type": HAZARD_TYPE_CLIFF})
    # Note that zero is not a possible value as an object placed right up to the sensor
    # produces distance of ~ +/- 2cm.  zero only shows up when the distance from sensor
    # is far away (> 100cm). I think its from refraction echos. Exclude zero.
    if 0 < left_front_dist < SIDE_SENSOR_MIN_DIST:
        hazards.append({"sensor": LEFT_FRONT_SENSOR, "type": HAZARD_TYPE_COLLISION})

    if right_front_dist > SIDE_SENSOR_MAX_DIST:
        hazards.append({"sensor": RIGHT_FRONT_SENSOR, "type": HAZARD_TYPE_CLIFF})
    if 0 < right_front_dist < SIDE_SENSOR_MIN_DIST:
        hazards.append({"sensor": RIGHT_FRONT_SENSOR, "type": HAZARD_TYPE_COLLISION})

    if front_cliff_dist > FRONT_SENSOR_MAX_DIST:
        hazards.append({"sensor": FRONT_CLIFF_SENSOR, "type": HAZARD_TYPE_CLIFF})

    if 0 < front_dist < FRONT_SENSOR_MIN_DIST:
        print(f"{front_dist=}")
        hazards.append({"sensor": FRONT_SENSOR, "type": HAZARD_TYPE_COLLISION})

    return hazards


async def provide_state():
    last_message = ""
    while True:
        try:
            log.info(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                await messages.send_identity(websocket, "hazards")
                while True:
                    # query the sensors for distances
                    distances = get_distances()
                    front_hazards = detect_hazards_front(distances)
                    message = json.dumps(
                        {
                            "type": "updateState",
                            "data": {
                                "hazards": {
                                    "front": front_hazards,
                                    # "distances": distances,
                                }
                            },
                        }
                    )
                    if message != last_message:
                        if constants.LOG_ALL_MESSAGES:
                            log.info(f"sending: {message}")
                        await websocket.send(message)
                    last_message = message
                    await asyncio.sleep(0.01)
        except:
            traceback.print_exc()

        log.info("socket disconnected.  Reconnecting in 5 sec...")
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

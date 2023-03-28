import time
import json
import asyncio
import traceback
import websockets

import board
import adafruit_tca9548a
import adafruit_vl53l4cd

from commons import constants, messages, log

FRONT_SENSORS_BASE_INDEX = 0
REAR_SENSORS_BASE_INDEX = 3

FRONT_DISTANCE_SENSOR = FRONT_SENSORS_BASE_INDEX + 2
REAR_DISTANCE_SENSOR = REAR_SENSORS_BASE_INDEX + 2

SENSOR_CHANNELS = [
    5,  # LEFT FRONT
    6,  # RIGHT FRONT
    7,  # CENTER FRONT
    3,  # LEFT REAR
    2,  # RIGHT REAR
    4,  # CENTER REAR
]

HAZARD_TYPE_COLLISION = "collision"
HAZARD_TYPE_CLIFF = "cliff"

SIDE_SENSOR_MIN_DIST = 6
SIDE_SENSOR_MAX_DIST = 15
CENTER_SENSOR_MIN_DIST = 5


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


def detect_hazards(distances, base_sensor_index):
    hazards = []
    [left_dist, right_dist, center_dist] = distances[
        base_sensor_index : base_sensor_index + 3
    ]
    [left_sensor, right_sensor, center_sensor] = range(
        base_sensor_index, base_sensor_index + 3
    )

    if left_dist > SIDE_SENSOR_MAX_DIST:
        hazards.append({"sensor": left_sensor, "type": HAZARD_TYPE_CLIFF})

    # Note that zero is not a possible value as an object placed right up to the sensor
    # produces distance of ~2cm.  zero only shows up when the distance from sensor
    # is far away (> 100cm). I think its from refraction echos. Exclude zero.
    if 0 < left_dist < SIDE_SENSOR_MIN_DIST:
        hazards.append({"sensor": left_sensor, "type": HAZARD_TYPE_COLLISION})

    if right_dist > SIDE_SENSOR_MAX_DIST:
        hazards.append({"sensor": right_sensor, "type": HAZARD_TYPE_CLIFF})
    if 0 < right_dist < SIDE_SENSOR_MIN_DIST:
        hazards.append({"sensor": right_sensor, "type": HAZARD_TYPE_COLLISION})

    if 0 < center_dist < CENTER_SENSOR_MIN_DIST:
        hazards.append({"sensor": center_sensor, "type": HAZARD_TYPE_COLLISION})

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
                    front_hazards = detect_hazards(distances, FRONT_SENSORS_BASE_INDEX)
                    rear_hazards = detect_hazards(distances, REAR_SENSORS_BASE_INDEX)

                    message = json.dumps(
                        {
                            "type": "updateState",
                            "data": {
                                "hazards": {
                                    "front": front_hazards,
                                    "rear": rear_hazards,
                                },
                                "distances": {
                                    "front": distances[FRONT_DISTANCE_SENSOR],
                                    "rear": distances[REAR_DISTANCE_SENSOR],
                                },
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

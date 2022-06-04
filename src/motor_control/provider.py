from multiprocessing.dummy import Array
import time
import json
import asyncio
import traceback
import websockets
from adafruit_motorkit import MotorKit

from commons import constants, messages

kit = MotorKit(0x60)
left_motor = kit.motor3
right_motor = kit.motor4
feed_motor = kit.motor1

last_feed_requested_at = 0


async def send_motor_state(websocket):
    await messages.send_state_update(websocket, {
        "motors": {
            "left": left_motor.throttle,
            "right": right_motor.throttle,
        }
    })


async def feeder_task(requestedAt):
    global last_feed_requested_at
    print(f"got feeder request: {requestedAt}")
    if requestedAt != last_feed_requested_at:
        feed_motor.throttle = 1
        await asyncio.sleep(1)
        feed_motor.throttle = -1
        await asyncio.sleep(1)
        feed_motor.throttle = 0
        last_feed_requested_at = requestedAt


async def provide_state():
    while True:
        try:
            print(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                # reset motors incase of restart due to crash
                left_motor.throttle = 0
                right_motor.throttle = 0
                feed_motor.throttle = 0

                await messages.send_identity(websocket, "motor_control")
                await messages.send_subscribe(websocket, ["throttles", "feeder"])
                async for message in websocket:
                    data = json.loads(message)
                    message_data = data.get("data")
                    if "throttles" in message_data:
                        left_throttle = min(
                            max(message_data["throttles"]["left"], -1), 1)
                        right_throttle = min(
                            max(message_data["throttles"]["right"], -1), 1)
                        print(
                            f"setting throttles ({left_throttle}, {right_throttle})")
                        left_motor.throttle = left_throttle
                        right_motor.throttle = right_throttle
                        await send_motor_state(websocket)
                    elif "feeder" in message_data:
                        asyncio.create_task(feeder_task(
                            message_data["feeder"]["requested_at"]))

                await asyncio.sleep(0.05)

        except:
            traceback.print_exc()

        print('socket disconnected.  Reconnecting in 5 sec...')
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

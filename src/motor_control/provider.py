from multiprocessing.dummy import Array
import time
import json
import asyncio
import traceback
import websockets
from adafruit_motorkit import MotorKit

from commons import constants, messages

kit = MotorKit(0x70)
left_motor = kit.motor1
right_motor = kit.motor2
feed_motor = kit.motor4


async def send_motor_state(websocket):
    await messages.send_state_update(websocket, {
        "motors": {
            "left": left_motor.throttle,
            "right": right_motor.throttle,
        }
    })


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
                await messages.send_subscribe(websocket, ["throttles"])
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

                await asyncio.sleep(0.05)

        except:
            traceback.print_exc()

        print('socket disconnected.  Reconnecting in 5 sec...')
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

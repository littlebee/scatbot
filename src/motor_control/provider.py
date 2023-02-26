import time
import json
import asyncio
import traceback
import websockets
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

from commons import constants, messages

# need freq of 50hz for servo (I think)
kit = MotorKit(constants.MOTOR_ADDRESS)
left_motor = kit.motor3
right_motor = kit.motor4

servoKit = ServoKit(channels=16, address=constants.MOTOR_ADDRESS)
feed_servo = servoKit.servo[14]
last_feed_requested_at = 0

SERVO_REST_ANGLE = 40
SERVO_OPEN_ANGLE = 140


async def send_motor_state(websocket):
    await messages.send_state_update(
        websocket,
        {
            "motors": {
                "left": left_motor.throttle,
                "right": right_motor.throttle,
            }
        },
    )


async def feeder_task(requestedAt):
    global last_feed_requested_at
    if requestedAt != last_feed_requested_at:
        print(f"got feeder request: {requestedAt}")
        feed_servo.angle = 0
        await asyncio.sleep(0.25)
        feed_servo.angle = 110
        await asyncio.sleep(0.5)
        feed_servo.angle = SERVO_REST_ANGLE
        last_feed_requested_at = requestedAt


async def provide_state():
    while True:
        try:
            print(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                # reset motors incase of restart due to crash
                left_motor.throttle = 0
                right_motor.throttle = 0
                feed_servo.angle = SERVO_REST_ANGLE

                await messages.send_identity(websocket, "motor_control")
                await messages.send_subscribe(websocket, ["throttles", "feeder"])
                async for message in websocket:
                    data = json.loads(message)
                    message_data = data.get("data")
                    if "throttles" in message_data:
                        left_throttle = min(
                            max(message_data["throttles"]["left"], -1), 1
                        )
                        right_throttle = min(
                            max(message_data["throttles"]["right"], -1), 1
                        )
                        print(f"setting throttles ({left_throttle}, {right_throttle})")
                        left_motor.throttle = left_throttle
                        right_motor.throttle = right_throttle
                        await send_motor_state(websocket)
                    elif "feeder" in message_data:
                        asyncio.create_task(
                            feeder_task(message_data["feeder"]["requested_at"])
                        )

                await asyncio.sleep(0.05)

        except:
            traceback.print_exc()

        print("socket disconnected.  Reconnecting in 5 sec...")
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

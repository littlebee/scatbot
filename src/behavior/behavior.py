""" This is the behavior subsystem """
import json
import asyncio
import traceback

import websockets

from commons import constants as c, messages, shared_state, log

from behavior.tasks.follow_task import follow_task
from behavior.behavior_state import send_state_update


TASKS = {
    # in remote control mode, there is nothing to do; the UI directly controls
    # lights, sounds, motors and feeder
    c.BEHAVIORS.RC.value: None,
    # Track people or pets (rotate only)
    c.BEHAVIORS.TRACK.value: follow_task,
    # Follow people or pets
    c.BEHAVIORS.FOLLOW.value: follow_task,
}

current_behavior = c.DEFAULT_BEHAVIOR
current_behavior_task = None


async def maybe_switch_behavior(websocket):
    global current_behavior
    global current_behavior_task

    new_behavior = shared_state.state["behave"]
    if new_behavior == current_behavior or new_behavior not in c.VALID_BEHAVIORS:
        return

    current_behavior = new_behavior

    if current_behavior_task:
        current_behavior_task.cancel()

    new_behavior_task = TASKS[new_behavior]
    if new_behavior_task:
        current_behavior_task = asyncio.create_task(new_behavior_task(websocket))
    else:
        # no behavior is RC mode
        current_behavior_task = None

    log.info(f"switched behavior mode to {current_behavior}")
    await send_state_update(
        websocket,
        {"mode": current_behavior, "targetAcquired": False, "targetBoundingBox": []},
    )


async def state_task():
    while True:
        try:
            log.info(f"connecting to {c.HUB_URI}")
            async with websockets.connect(c.HUB_URI) as websocket:
                await messages.send_identity(websocket, "behavior")
                await messages.send_subscribe(
                    websocket,
                    [
                        "behave",
                        "compass",
                        "depth_map",
                        "recognition",
                        "hazards",
                        "distances",
                    ],
                )
                await messages.send_get_state(websocket)
                async for message in websocket:
                    json_data = json.loads(message)
                    message_type = json_data.get("type")
                    message_data = json_data.get("data")

                    if c.LOG_ALL_MESSAGES:
                        log.info(f"got {message_type}: {message_data}")

                    if message_type in ["stateUpdate", "state"]:
                        shared_state.update_state_from_message_data(message_data)

                    await maybe_switch_behavior(websocket)

        except:
            traceback.print_exc()

        log.info("socket disconnected.  Reconnecting in 5 sec...")
        await asyncio.sleep(5)


async def start():
    _state_task = asyncio.create_task(state_task())
    await asyncio.wait([_state_task])


asyncio.run(start())

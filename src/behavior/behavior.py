""" This is the behavior subsystem """
import signal
import sys
import json
import asyncio
import traceback

import websockets

from commons import constants, messages, shared_state
from commons.enums import BEHAVIORS, DEFAULT_BEHAVIOR, VALID_BEHAVIORS

from tasks.follow_task import follow_task


TASKS = {
    # in remote control mode, there is nothing to do; the UI directly controls
    # lights, sounds, motors and feeder
    BEHAVIORS.RC: None,
    # Follow people or pets
    BEHAVIORS.FOLLOW: follow_task,
}

current_behavior = DEFAULT_BEHAVIOR
current_behavior_task = None


def hup_handler():
    global should_exit

    print("caught sighup")
    should_exit = True
    raise OSError("Received shutdown signal!")


signal.signal(signal.SIGHUP, hup_handler)


def log(message):
    """Flush message to console"""
    print(message)
    sys.stdout.flush()


async def maybe_switch_behavior():
    global current_behavior
    global current_behavior_task

    new_behavior = shared_state["behavior"]
    if new_behavior == current_behavior or new_behavior not in VALID_BEHAVIORS:
        return

    current_behavior = new_behavior

    if current_behavior_task:
        await current_behavior_task.cancel()

    new_behavior_task = TASKS[new_behavior]
    if new_behavior_task:
        current_behavior_task = asyncio.create_task(new_behavior_task)
    else:
        current_behavior_task = None


async def state_task():
    try:
        while not should_exit:
            try:
                log(f"connecting to {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    await messages.send_identity(websocket, "behavior")
                    await messages.send_subscribe(
                        websocket, ["behavior", "compass", "depth_map", "recognition"]
                    )
                    await messages.send_get_state(websocket)
                    async for message in websocket:
                        json_data = json.loads(message)
                        message_type = json_data.get("type")
                        message_data = json_data.get("data")

                        if messages.LOG_ALL_MESSAGES:
                            log(f"got {message_type}: {message_data}")

                        if message_type in ["stateUpdate", "state"]:
                            shared_state.update_state_from_message_data(message_data)

                        await maybe_switch_behavior()

            except:
                traceback.print_exc()

            if should_exit:
                log("got shutdown signal.  exiting.")
            else:
                log("socket disconnected.  Reconnecting in 5 sec...")
                await asyncio.sleep(5)

    except Exception as e:
        log(f"got exception on async loop. Exiting. {e}")

    finally:
        pass


async def start():
    _state_task = asyncio.create_task(state_task())
    await asyncio.wait([_state_task])


asyncio.run(start())

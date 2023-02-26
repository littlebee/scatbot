""" This is the behavior subsystem """
import signal
import sys
import json
import asyncio
import traceback

import websockets

from commons import constants, messages, shared_state


current_websocket = None

should_exit = False


def hup_handler():
    global should_exit

    print("caught sighup")
    should_exit = True
    raise OSError("Received shutdown signal!")


# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGHUP, hup_handler)


def log(message):
    """Flush message to console"""
    print(message)
    sys.stdout.flush()


async def state_task():
    global current_websocket

    try:
        while not should_exit:
            try:
                log(f"connecting to {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    current_websocket = websocket
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


async def behavior_task():
    """
    This task watches for changes to behavior mode in shared state and calls the
    appropriate BehaviorTask loop function
    """


async def start():
    _state_task = asyncio.create_task(state_task())
    await asyncio.wait([_state_task])


asyncio.run(start())

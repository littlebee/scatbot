import os
import signal
import sys
import socket
import json
import pygame
import websockets
import asyncio
import traceback
import subprocess
import board
from digitalio import DigitalInOut, Direction, Pull

from commons import constants, messages, shared_state

white = (255, 255, 255)
black = (0, 0, 0)

reset_button = DigitalInOut(board.D17)
reset_button.direction = Direction.INPUT
reset_button.pull = Pull.UP

os.putenv('SDL_FBDEV', '/dev/fb1')
print("Initializing pygame...")
pygame.init()
print("Setting pygame display mode...")
screen = pygame.display.set_mode((240, 240))
print("Initialized.")
screen_width = screen.get_width()
screen_height = screen.get_height()

pygame.mouse.set_visible(False)
screen.fill(black)

large_font = pygame.font.SysFont('timesnewroman',  30)
small_font = pygame.font.SysFont('timesnewroman',  20)

current_websocket = None

should_exit = False


def handler(signum, frame):
    global should_exit

    print('caught sighup')
    should_exit = True
    raise OSError("Received shutdown signal!")


# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGHUP, handler)


def log(message):
    print(message)
    sys.stdout.flush()


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr
    except Exception as e:
        log(f"unable to get ip address. {e}")
        return "0.0.0.0"


async def rc_behavior_task():
    global should_exit

    # await render_splash()
    while not should_exit:
        await render()

        if not reset_button.value:
            os.system('shutdown now')

        await asyncio.sleep(1)

    log("exiting ui task")


async def state_task():
    global current_websocket
    global should_exit

    try:
        while not should_exit:
            try:
                log(f"connecting to {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    current_websocket = websocket
                    await messages.send_identity(websocket, "onboard_ui")
                    await messages.send_subscribe(websocket, ["system_stats", "battery"])
                    await messages.send_get_state(websocket)
                    async for message in websocket:
                        json_data = json.loads(message)
                        message_type = json_data.get("type")
                        message_data = json_data.get('data')

                        if messages.LOG_ALL_MESSAGES:
                            log(f"got {message_type}: {message_data}")

                        if message_type in ["stateUpdate", "state"]:
                            shared_state.update_state_from_message_data(
                                message_data)

            except:
                traceback.print_exc()

            if should_exit:
                log('got shutdown signal.  exiting.')
            else:
                log('socket disconnected.  Reconnecting in 5 sec...')
                await asyncio.sleep(5)

    except Exception as e:
        log(f"got exception on async loop. Exiting. {e}")

    finally:
        pass


async def start():
    recvTask = asyncio.create_task(state_task())
    uiTask = asyncio.create_task(ui_task())
    await asyncio.wait([recvTask, uiTask])

asyncio.run(start())

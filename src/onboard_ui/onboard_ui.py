import sys
import os
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


async def render_splash():
    global screen
    global screen_width
    global screen_height

    buffer = pygame.Surface((screen_width, screen_height))
    splash = pygame.image.load(os.path.dirname(
        sys.argv[0])+'/onboard_ui/media/images/scatbot-splash.bmp')
    # splash = pygame.transform.rotate(splash, args.rotation)
    screen.blit(splash, ((screen_width / 2) - (splash.get_width() / 2),
                (screen_height / 2) - (splash.get_height() / 2)))

    pygame.display.update()
    await asyncio.sleep(10)
    screen.fill(black)
    pygame.display.update()


async def render():
    global screen
    global screen_width
    global screen_height

    try:
        (cpu_temp, *rest) = [
            int(i) / 1000 for i in
            os.popen(
                'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
        ]

        screen.fill(black)
        text = small_font.render("Network:", True, white, black)
        screen.blit(text, (0, 0))

        text = large_font.render(
            f"{socket.gethostname()}.local", True, white, black)
        screen.blit(text, (10, 22))

        text = large_font.render(
            get_ip_address(), True, white, black)
        screen.blit(text, (10, 58))

        wifiSsid = subprocess.run(
            ["iwgetid", "-r"], stdout=subprocess.PIPE).stdout
        text = large_font.render(wifiSsid, True, white, black)
        screen.blit(text, (10, 92))

        text = small_font.render("CPU: ", True, white, black)
        screen.blit(text, (0, 126))

        cpu_util = shared_state.state["system_stats"]["cpu_util"]
        text = large_font.render(
            f"{cpu_util:.1f}%", True, white, black)
        screen.blit(text, (10, 148))

        cpu_temp = shared_state.state["system_stats"]["cpu_temp"]
        text = large_font.render(
            f"{cpu_temp:.1f}°", True, white, black)
        screen.blit(text, (100, 148))

        text = small_font.render("Battery: ", True, white, black)
        screen.blit(text, (0, 180))
        battery_voltage = shared_state.state["battery"]["voltage"]
        battery_current = shared_state.state["battery"]["current"]
        text = large_font.render(
            f"{battery_voltage:.1f}V@{battery_current:.1f}A", True, white, black)
        screen.blit(text, (10, 202))

        pygame.display.update()

    except Exception as e:
        print(f"could not get stats {e}")


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr
    except Exception as e:
        print(f"unable to get ip address. {e}")
        return "0.0.0.0"


async def ui_task():
    # await render_splash()
    while True:
        await render()

        if not reset_button.value:
            os.system('shutdown now')

        await asyncio.sleep(1)


async def state_task():
    global current_websocket

    try:
        while True:
            try:
                print(f"connecting to {constants.HUB_URI}", flush=True)
                async with websockets.connect(constants.HUB_URI) as websocket:
                    current_websocket = websocket
                    await messages.send_identity(websocket, "onboard_ui")
                    await messages.send_subscribe(websocket, ["system_stats", "battery"])
                    await messages.send_get_state(websocket)
                    async for message in websocket:
                        json_data = json.loads(message)
                        message_type = json_data.get("type")
                        message_data = json_data.get('data')
                        # print(f"got {message_type}: {message_data}")
                        if message_type in ["stateUpdate", "state"]:
                            shared_state.update_state_from_message_data(
                                message_data)
                        # print('getting next message')

            except:
                traceback.print_exc()

            print('socket disconnected.  Reconnecting in 5 sec...')
            await asyncio.sleep(5)
    except Exception as e:
        print(f"got exception on async loop. Exiting. {e}")
    finally:
        pygame.quit()


async def start():
    recvTask = asyncio.create_task(state_task())
    movementTask = asyncio.create_task(ui_task())
    await asyncio.wait([recvTask, movementTask])

asyncio.run(start())

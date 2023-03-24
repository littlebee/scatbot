import os
import signal
import sys
import json
import pygame
import websockets
import asyncio
import traceback
import board
from digitalio import DigitalInOut, Direction, Pull

from commons import constants, log, messages, shared_state
from onboard_ui.leds import update_leds
from onboard_ui.system_info import render_system_info
import onboard_ui.styles as styles

reset_button = DigitalInOut(board.D17)
reset_button.direction = Direction.INPUT
reset_button.pull = Pull.UP

os.putenv("SDL_FBDEV", "/dev/fb1")
print("Initializing pygame...")
pygame.init()
print("Setting pygame display mode...")
screen = pygame.display.set_mode((240, 240))
print("Initialized.")
screen_width = screen.get_width()
screen_height = screen.get_height()

pygame.mouse.set_visible(False)
screen.fill(styles.BLACK)

current_websocket = None

should_exit = False


def handler(signum, frame):
    global should_exit

    print("caught sighup")
    should_exit = True
    raise OSError("Received shutdown signal!")


# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGHUP, handler)


async def render_splash():
    global screen
    global screen_width
    global screen_height

    splash = pygame.image.load(
        os.path.dirname(sys.argv[0]) + "/onboard_ui/media/images/scatbot-splash.bmp"
    )
    # splash = pygame.transform.rotate(splash, args.rotation)
    screen.blit(
        splash,
        (
            (screen_width / 2) - (splash.get_width() / 2),
            (screen_height / 2) - (splash.get_height() / 2),
        ),
    )

    pygame.display.update()
    await asyncio.sleep(10)
    screen.fill(styles.BLACK)
    pygame.display.update()


async def render():
    global screen
    global screen_width
    global screen_height

    try:
        screen.fill(styles.BLACK)
        render_system_info(screen)
        pygame.display.update()

    except Exception as e:
        traceback.print_exc()
        log.error(f"could not get stats {e}")


async def ui_task():
    global should_exit

    # await render_splash()
    while not should_exit:
        await render()
        if not reset_button.value:
            os.system("shutdown now")

        await asyncio.sleep(1)

    log.info("exiting ui task")


async def led_task():
    while not should_exit:
        try:
            update_leds()
            await asyncio.sleep(0.25)
        except Exception as e:
            traceback.print_exc()
            log.error(f"error in led_task: {e}")


async def state_task():
    global current_websocket
    global should_exit

    try:
        while not should_exit:
            try:
                log.info(f"connecting to {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    current_websocket = websocket
                    await messages.send_identity(websocket, "onboard_ui")
                    await messages.send_subscribe(
                        websocket, ["system_stats", "battery", "hazards"]
                    )
                    await messages.send_get_state(websocket)
                    async for message in websocket:
                        json_data = json.loads(message)
                        message_type = json_data.get("type")
                        message_data = json_data.get("data")

                        if constants.LOG_ALL_MESSAGES:
                            log.info(f"got {message_type}: {message_data}")

                        if message_type in ["stateUpdate", "state"]:
                            shared_state.update_state_from_message_data(message_data)

            except:
                traceback.print_exc()

            if should_exit:
                log.info("got shutdown signal.  exiting.")
            else:
                log.info("socket disconnected.  Reconnecting in 5 sec...")
                await asyncio.sleep(5)

    except Exception as e:
        log.error(f"got exception on async loop. Exiting. {e}")

    finally:
        pygame.quit()


async def start():
    tasks = []
    tasks.append(asyncio.create_task(state_task()))
    tasks.append(asyncio.create_task(ui_task()))
    tasks.append(asyncio.create_task(led_task()))
    await asyncio.wait(tasks)


asyncio.run(start())

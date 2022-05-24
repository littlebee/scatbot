import sys
import os
import socket
import time
import pygame
import websockets
import asyncio
import traceback
import subprocess
import psutil

from commons import constants, messages

white = (255, 255, 255)
black = (0, 0, 0)


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


async def render_network_stats():
    global screen
    global screen_width
    global screen_height

    (cpu_temp, *rest) = [
        int(i) / 1000 for i in
        os.popen(
            'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
    ]

    screen.fill(black)
    text = small_font.render("Wifi SSID:", True, white, black)
    screen.blit(text, (0, 0))
    wifiSsid = subprocess.run(["iwgetid", "-r"], stdout=subprocess.PIPE).stdout
    text = large_font.render(wifiSsid, True, white, black)
    screen.blit(text, (10, 22))

    text = small_font.render("Host name:", True, white, black)
    screen.blit(text, (0, 60))
    text = large_font.render(
        f"{socket.gethostname()}.local", True, white, black)
    screen.blit(text, (10, 82))

    text = small_font.render("IP address:", True, white, black)
    screen.blit(text, (0, 120))
    text = large_font.render(
        get_ip_address(), True, white, black)
    screen.blit(text, (10, 142))

    text = small_font.render("CPU: ", True, white, black)
    screen.blit(text, (0, 180))
    text = large_font.render(
        f"{psutil.cpu_percent():.1f}%", True, white, black)
    screen.blit(text, (10, 202))
    text = large_font.render(
        f"{cpu_temp:.1f}°", True, white, black)
    screen.blit(text, (100, 202))

    pygame.display.update()


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


async def ui_task():
    await render_splash()
    await render_network_stats()

    try:
        while True:
            try:
                print(f"connecting to {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    await messages.send_identity(websocket, "onboard_ui")
                    while True:
                        await render_network_stats()
                        # TODO : call function to handle button interactions
                        #   and screen updates.   Also reduce sleep duration below.
                        await asyncio.sleep(2)
            except:
                traceback.print_exc()

            print('socket disconnected.  Reconnecting in 5 sec...')
            await asyncio.sleep(5)
    except Exception as e:
        print(f"got exception on async loop. Exiting. {e}")
    finally:
        pygame.quit()

asyncio.run(ui_task())

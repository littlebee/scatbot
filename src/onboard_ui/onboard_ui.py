import sys
import os
import socket
import time
import pygame

white = (255, 255, 255)
black = (0, 0, 0)

# initialize the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
screen = pygame.display.set_mode((240, 240))
screen_width = screen.get_width()
screen_height = screen.get_height()


pygame.mouse.set_visible(False)
screen.fill(black)


buffer = pygame.Surface((screen_width, screen_height))
splash = pygame.image.load(os.path.dirname(
    sys.argv[0])+'/onboard_ui/media/images/scatbot-splash.bmp')
# splash = pygame.transform.rotate(splash, args.rotation)
screen.blit(splash, ((screen_width / 2) - (splash.get_width() / 2),
            (screen_height / 2) - (splash.get_height() / 2)))

pygame.display.update()
time.sleep(10)

screen.fill(black)
pygame.display.update()

large_font = pygame.font.SysFont('timesnewroman',  30)
small_font = pygame.font.SysFont('timesnewroman',  20)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


while True:
    text = small_font.render("Host name:", True, white, black)
    screen.blit(text, (0, 0))
    text = large_font.render(
        f"{socket.gethostname()}.local", True, white, black)
    screen.blit(text, (10, 22))

    text = small_font.render("IP address:", True, white, black)
    screen.blit(text, (0, 60))
    text = large_font.render(get_ip_address(), True, white, black)
    screen.blit(text, (10, 82))

    pygame.display.update()
    time.sleep(60)

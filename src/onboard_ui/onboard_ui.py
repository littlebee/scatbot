import sys
import os
import time
import pygame

# initialize the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
screen = pygame.display.set_mode((240, 240))
screen_width = screen.get_width()
screen_height = screen.get_height()

pygame.mouse.set_visible(False)
screen.fill((0, 0, 0))

buffer = pygame.Surface((screen_width, screen_height))

try:
    splash = pygame.image.load(os.path.dirname(
        sys.argv[0])+'/media/images/scatbot-splash.bmp')
    # splash = pygame.transform.rotate(splash, args.rotation)
    screen.blit(splash, ((screen_width / 2) - (splash.get_width() / 2),
                (screen_height / 2) - (splash.get_height() / 2)))
except pygame.error:
    pass

pygame.display.update()

while True:
    time.sleep(60)

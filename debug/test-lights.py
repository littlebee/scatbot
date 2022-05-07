#!/usr/bin/env python3
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D12, 1)
while True:
    print("red")
    pixels[0] = (255, 0, 0)
    time.sleep(5)
    print("green")
    pixels[0] = (0, 255, 0)
    time.sleep(5)
    print("blue")
    pixels[0] = (0, 0, 255)
    time.sleep(5)
    print("white")
    pixels[0] = (255, 255, 255)
    time.sleep(5)
    print("black")
    pixels[0] = (0, 0, 0)
    time.sleep(5)

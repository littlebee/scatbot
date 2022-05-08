#!/usr/bin/env python3
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D12, 2)
while True:
    for i in range(0, 2):
        print(f"pixel {i}")
        print("red")
        pixels[i] = (255, 0, 0)
        time.sleep(5)
        print("green")
        pixels[i] = (0, 255, 0)
        time.sleep(5)
        print("blue")
        pixels[i] = (0, 0, 255)
        time.sleep(5)
        print("white")
        pixels[i] = (255, 255, 255)
        time.sleep(5)
        print("black")
        pixels[i] = (0, 0, 0)
        time.sleep(5)

# scatbot

A robot to follow my dog around and give her treats

<img src="https://github.com/littlebee/scatbot/blob/fdfa67ec1966cedb2e5a322f2bc2d7778dd695b0/docs/img/scatbot-pi-design.png"
     alt="design image"
     style="float: right; margin-right: 10px; width: 400px;" />

I originally got the idea for scatbot watching my dog interact with the Roomba. She seemed disappointed and frustrated that El Roomba just went about his business as if she wasn't sitting right there with the ball the robot had just pushed out from under the couch. How rude.

Scatbot is designed to be about the same height as a Roomba (< 100mm) so that it can fit under most of my furniture.

The idea is that it will be R/C or autonomous with several autonomous modes like "Follow" or "Hide and Seek".

Originally I started designing, and even built an alpha-1 prototype, around the Nvidia Jetson Nano, but a couple of things doomed that design. Space! is so important and the Nano is not very small when you add on it's big heat sink and fan. Also the torture of getting all of the 3rd party software (tensor flow, opencv, adafruit motorkit, ...) working together was a brutal dungeon craw.

It runs on a Raspberry PI 4b w/4GB. The [Adafruit Braincraft hat](https://www.adafruit.com/product/4374) provides the onboard-ui, audio amplifier and a few LEDs that are used for expressive behaviors.

## See also

Spreadsheet of parts:
https://docs.google.com/spreadsheets/d/1Sh4O05_kYhsgo-QO83rhAAbxgSdKjL1iUw-a6iWCc7w/edit?usp=sharing

Fusion 360 designs:
https://ymail2984.autodesk360.com/g/shares/SH35dfcQT936092f0e436a5991538bbd4822

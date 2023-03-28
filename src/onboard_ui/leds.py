import board
import adafruit_dotstar as dotstar

from commons import shared_state

# These are the leds on the Adafruit Braincraft hat
DOTS = dotstar.DotStar(board.D6, board.D5, 3, brightness=0.2)

# indexes into dots
LEFT_DOT = 0
CENTER_DOT = 1
RIGHT_DOT = 2

# values for dots are numeric triples in the form (g, b, r)
RED = (0, 0, 128)
GREEN = (128, 0, 0)
BLACK = (0, 0, 0)

DOTS.fill(BLACK)


def update_leds():
    hazards = shared_state.state["hazards"]

    if "front" in hazards and len(hazards["front"]) > 0:
        DOTS[RIGHT_DOT] = RED
    else:
        DOTS[RIGHT_DOT] = BLACK

    if "rear" in hazards and len(hazards["rear"]) > 0:
        DOTS[LEFT_DOT] = RED
    else:
        DOTS[LEFT_DOT] = BLACK

    DOTS[CENTER_DOT] = BLACK

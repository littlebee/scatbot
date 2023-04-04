from enum import Enum
import os


def env_string(name, default):
    env_val = os.getenv(name) or str(default)
    return env_val


def env_int(name, default):
    try:
        return int(env_string(name, default))
    except:
        return default


def env_float(name, default):
    try:
        return float(env_string(name, default))
    except:
        return default


def env_bool(name, default):
    value = env_string(name, default).lower()
    if value in ("true", "1"):
        return True
    else:
        return False


# Image capture dims in pixels
VISION_HEIGHT = 480
VISION_WIDTH = 640
# in degrees; depends on camera; RPi v2 cam is 62deg
VISION_FOV = 62

#
# Add I2C Addresses for all devices here for easy lookup
#
BATTERY_I2C_ADDRESS = 0x40
COMPASS_I2C_ADDRESS = 0x60
MOTOR_I2C_ADDRESS = 0x70
# this is the I2c address of a TCA9548A i2c multiplexer that is
# connected to several ToF sensors in front and rear bumpers
# Note that the preconf address of the Adafruit breakout is 0x70
# which conficts with the Motor I2C addr and I changed by jumpering
# the A0 solder pads on back of the board
MULTI_TOF_I2C_ADDRESS = 0x71


# Raspberry Pi 4 camera
CAMERA_CHANNEL_PICAM = 0
# realsense RGB camera channel (USB)
CAMERA_CHANNEL_RS = 4
# which v4l channel  is the rgb image read from
CAMERA_CHANNEL = env_int("CAMERA_CHANNEL", CAMERA_CHANNEL_PICAM)
# realsense depth camera channel
CAMERA_CHANNEL_RS_DEPTH = 2  # maybe??

DISABLE_DEPTH_PROVIDER = env_bool("DISABLE_DEPTH_PROVIDER", False)
DISABLE_RECOGNITION_PROVIDER = env_bool("DISABLE_RECOGNITION_PROVIDER", False)

# realsense_vision module can do recognition (object detection) from the rs color
# image stream, but....  It performs really poorly
DISABLE_REALSENSE_RECOGNITION = (
    env_bool("DISABLE_REALSENSE_RECOGNITION", True) or DISABLE_RECOGNITION_PROVIDER
)

# use coral USB tpu
DISABLE_CORAL_TPU = env_bool("DISABLE_CORAL_TPU", False)
# num cpu threads to use for tensor flow lite
TFLITE_THREADS = env_int("TFLITE_THREADS", 4)
# location of models
TFLITE_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data/tflite")
)


# delay between sampling compass; 0.5 = ~20Hz
COMPASS_SAMPLE_INTERVAL = 0.05
# min absolute difference between samples to send to hub
COMPASS_CHANGE_TOLERANCE = 0.1
# true north / magnetic north offset (based on factory calibrated cmps14)
COMPASS_MAGNETIC_OFFSET = env_int("COMPASS_MAGNETIC_OFFSET", 144)

# how often the ina219 is sampled for batter voltage
BATTERY_SAMPLE_INTERVAL = 1  # 1Hz
# below what voltage the battery subsystem issues a `sudo shutdown now`
BATTERY_SHUTDOWN_VOLTAGE = 5.5

# min time in seconds, between publishing depth map data to central hub
DEPTH_PUBLISH_INTERVAL = 0.01  # 19fps
# divide depth map into this many horz sections
DEPTH_MAP_SECTION_WIDTH = 5
# divide depth map into this many vert sections
DEPTH_MAP_SECTION_HEIGHT = 5
# min change in min distance before section map will republish
DEPTH_MAP_CHANGE_TOLERACE = 1

# Connect to central hub websocket
HUB_PORT = env_int("HUB_PORT", 5000)
HUB_URI = f"ws://127.0.0.1:{HUB_PORT}/ws"

LOG_ALL_MESSAGES = env_bool("LOG_ALL_MESSAGES", False)

# delay between sampling compass; 0.5 = ~2Hz
SYSTEM_STATS_SAMPLE_INTERVAL = 0.5

# vision http server
VISION_PORT = 5001

# depth http server (diff from vision so they can run on the same sbc)
DEPTH_PORT = 5002

# For Raspberry Pi4 w/ 64bit OS, this should be 1
I2C_BUS = 1


class BEHAVIORS(Enum):
    # Remote control mode
    RC = 0
    # Track in place any person, cat or dog it sees (autonomous)
    TRACK = 1
    # Follow any person, cat or dog it sees (autonomous)
    FOLLOW = 2


VALID_BEHAVIORS = set(item.value for item in BEHAVIORS)
DEFAULT_BEHAVIOR = 0


# Class labels from official PyTorch documentation for the pretrained model
# Note that there are some N/A's
# for complete list check https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
# we will use the same list for this notebook
COCO_INSTANCE_CATEGORY_NAMES = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

# object detection threshold percentage; higher = greater confidence
OBJECT_DETECTION_THRESHOLD = 0.5

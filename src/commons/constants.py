import os


# which v4l channel  is the rgb image read from
CAMERA_CHANNEL_RGB = 4 if not os.getenv(
    'CAMERA_CHANNEL') else int(os.getenv('CAMERA_CHANNEL'))
# IDK??
CAMERA_CHANNEL_DEPTH = 2  # maybe??

# Compass I2C address
COMPASS_ADDRESS = 0x60
# delay between sampling compass; 0.5 = ~20Hz
COMPASS_SAMPLE_INTERVAL = 0.05
# min absolute difference between samples to send to hub
COMPASS_CHANGE_TOLERANCE = 0.1
# true north / magnetic north offset
COMPASS_MAGNETIC_OFFSET = -67.2

# how often the ina219 is sampled for batter voltage
BATTERY_SAMPLE_INTERVAL = 1  # 1Hz
# below what voltage the battery subsystem issues a `sudo shutdown now`
BATTERY_SHUTDOWN_VOLTAGE = 5.5

# min time in seconds, between publishing depth map data to central hub
DEPTH_PUBLISH_INTERVAL = 0.05  # 19fps
# divide depth map into this many horz sections
DEPTH_MAP_SECTION_WIDTH = 5
# divide depth map into this many vert sections
DEPTH_MAP_SECTION_HEIGHT = 5
# min change in min distance before section map will republish
DEPTH_MAP_CHANGE_TOLERACE = 1

# Connect to central hub websocket
HUB_PORT = 5000
HUB_URI = f"ws://127.0.0.1:{HUB_PORT}/ws"

# delay between sampling compass; 0.5 = ~2Hz
SYSTEM_STATS_SAMPLE_INTERVAL = 0.5

# vision http server
VISION_PORT = 5001

# For Raspberry Pi4 w/ 64bit OS, this should be 1
I2C_BUS = 1

# Motor controller I2C addr
MOTOR_ADDRESS = 0x70


# Class labels from official PyTorch documentation for the pretrained model
# Note that there are some N/A's
# for complete list check https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
# we will use the same list for this notebook
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

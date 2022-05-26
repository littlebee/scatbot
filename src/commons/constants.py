
# which v4l channel  is the rgb image read from
CAMERA_CHANNEL_RGB = 4
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

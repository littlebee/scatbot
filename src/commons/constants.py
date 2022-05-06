
# which v4l channel  is the rgb image read from
CAMERA_CHANNEL_RGB = 4
# IDK??
CAMERA_CHANNEL_DEPTH = 2  # maybe??

# Compass I2C address
COMPASS_ADDRESS = 0x60
# delay between sampling compass; 0.01 = ~90Hz
COMPASS_SAMPLE_INTERVAL = 0.01
# min absolute difference between samples to send to hub
COMPASS_CHANGE_TOLERANCE = 0.1
# true north / magnetic north offset
COMPASS_MAGNETIC_OFFSET = -67.2

# Connect to central hub websocket
HUB_URI = "ws://127.0.0.1/ws"

# For Raspberry Pi4 w/ 64bit OS, this should be 1
I2C_BUS = 1

# Motor controller I2C addr
MOTOR_ADDRESS = 0x70

import time
import json

SHARED_STATE = {
    # which behavior - RC, hide $ seek, follow
    "behavior": 0,
    # feedback about what behavior is doing
    "behavior_status": "offline",

    # heading
    "compass": 0,

    # depth map - array of mm distance from camera per pixel
    "depth_map": [],

    # recognized objects from pytorch
    "inference": [
        # this is a array of
        #  {
        #     "classificaton": "dog",
        #     "bounding_box": [0, 0, 0, 0],
        #     "confidence": 90
        #  }
    ],
    "hub_stats": {
        "state_updates_recv": 0
    },
    "system_stats": {
        "cpu_util": 0,
        "cpu_temp": 0,
        "ram_util": 0,
    }
}

# these are intended to be semi-constant and calibrated values
CONFIG = {
    # This is the difference between magnetic north (as read by the
    # tilt compensated compass) and true north
    "headingOffset": 28,

}


def serializeState():
    return json.dumps({"type": "state", "data": SHARED_STATE})


def serializeConfig():
    return json.dumps({"type": "config", "data": SHARED_STATE})


def update_state_from_message_data(message_data):
    for key in message_data:
        SHARED_STATE[key] = message_data[key]
        SHARED_STATE[f"{key}_updated_at"] = time.time()
    return

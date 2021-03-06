import time
import json

state = {
    "battery": {
        "voltage": 0,
        "current": 0,
    },

    # which behavior - RC, hide $ seek, follow
    "behavior": 0,

    # heading
    "compass": 0,

    # depth map - array of mm distance from camera per pixel
    "depth_map": {
        "min_distance": 0,
        "max_distance": 0,
        "section_map": [],
    },

    "feeder": {
        "requested_at": 0
    },

    "hub_stats": {
        "state_updates_recv": 0
    },

    # recognized objects from pytorch
    "recognition": [
        # this is a array of
        #  {
        #     "classificaton": "dog",
        #     "bounding_box": [0, 0, 0, 0],
        #     "confidence": 90
        #  }
    ],

    # This is separate from throttles which is the requested throttles.
    # This is what motor_control subsystem says the actual throttles are.
    "motors": {
        "left": 0,
        "right": 0,
        "feeder": 0
    },

    "system_stats": {
        "cpu_util": 0,
        "cpu_temp": 0,
        "ram_util": 0,
    },

    "subsystem_stats": {
        "central_hub": {
            "online": 1,
        },
        "compass": {
            "online": 0,
        },
        "motor_control": {
            "online": 0,
        },
        "onboard_ui": {
            "online": 0,
        },
        "system_stats": {
            "online": 0,
        },
        "vision": {
            "online": 0,
        },
        "recognition": {
            "online": 0,
        }
    },

    "throttles": {
        "left": 0,
        "right": 0,
    }

}

# these are intended to be semi-constant and calibrated values
CONFIG = {
    # This is the difference between magnetic north (as read by the
    # tilt compensated compass) and true north
    "headingOffset": 28,

}


def serializeState():
    return json.dumps({"type": "state", "data": state})


def serializeConfig():
    return json.dumps({"type": "config", "data": state})


def update_state_from_message_data(message_data):
    for key in message_data:
        state[key] = message_data[key]
        state[f"{key}_updated_at"] = time.time()
    return

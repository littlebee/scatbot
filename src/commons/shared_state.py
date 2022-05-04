import time
import json

SHARED_STATE = {
    # frustrating that enum is a class and makes this a complex object
    # that is not json serializable without a custom encoder :/
    # I don't want to use pickle on every single state broadcast loop
    "mode": 0,
    "compass": {
        "heading": 0,
    },
    "vision": {
        # this is a array of
        #  {
        #     "classificaton": "dog",
        #     "bounding_box": [0, 0, 0, 0],
        #     "confidence": 90
        #  }
        "last_seen": []
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

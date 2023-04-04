"""
    Provides all track and follow task behaviors
"""
import asyncio
import traceback

from commons import log, shared_state, constants as c
import behavior.behavior_state as state

CONFIDENCE_THRESHOLD = 0.5
TO_MATCH = ["person", "dog", "cat"]
VIEW_CENTER = (c.VISION_WIDTH / 2, c.VISION_HEIGHT / 2)

# how many pixels per one degree of rotation
# 640 pix / Raspberry Pi v2 cam  62 deg hz fov = 10.32
PIXELS_PER_DEGREE = c.env_int("PIXELS_PER_DEGREE", c.VISION_WIDTH / c.VISION_FOV)
# how many seconds to rotate per degree; TODO: maybe replace this with use of compass
SECONDS_PER_DEGREE = c.env_float("SECONDS_PER_DEGREE", 0.007)
# -1 to 1 speed of rotation
ROTATION_THROTTLE = c.env_float("ROTATION_THROTTLE", 0.5)
# how many degrees off center until we rotate
DEGREES_OFF_THRESHOLD = c.env_float("DEGREES_OFF_THRESHOLD", 2)
# minimum percent height of target / 480 to maintain
MIN_PERCENT_HEIGHT = 0.5
# maximum percent height of target / 480 to maintain
MAX_PERCENT_HEIGHT = 0.8


was_target_acquired = False


async def follow_task(websocket):
    """follow_task is a coroutine that runs when the follow `behave` mode is selected"""
    log.info("follow_task started")

    # task runs until canceled by ../behavior.py
    while True:
        try:
            target_object = acquire_target()
            await update_target_state(websocket, target_object)

            # returns True if centered on target, rotates if not
            if await center_on_target(websocket, target_object):
                if shared_state.state["behave"] == c.BEHAVIORS.FOLLOW.value:
                    await move_with_target(target_object)

            await asyncio.sleep(0.05)

        except Exception as e:
            log.error(f"caught exception in follow_task.py: {e}")
            traceback.print_exc()
            log.info("sleeping for 5 seconds before restarting task")
            await asyncio.sleep(5)


def acquire_target():
    recog_objects = [
        [obj, compute_dims(obj)]
        for obj in shared_state.state["recognition"]
        if obj["classification"] in TO_MATCH
        and obj["confidence"] >= CONFIDENCE_THRESHOLD
    ]

    # log.info(f"{recog_objects=}")

    target_object = None
    for obj in recog_objects:
        if not target_object:
            target_object = obj
        elif obj[1][2] > target_object[1][2]:
            target_object = obj

    return target_object


async def update_target_state(websocket, target_object):
    target_acquired = target_object is not None
    bounding_box = target_object[0]["boundingBox"] if target_acquired else []

    # any time we have a target, we want to update because the bounding
    # box most likely changed
    if not target_acquired and not was_target_acquired:
        return

    if target_acquired:
        log.info(f"follow_task: target acquired {target_object}")
    elif state.state["targetAcquired"]:
        log.info("follow_task: target lost")

    await state.send_target_state(websocket, target_acquired, bounding_box)


async def center_on_target(websocket, target_object):
    if target_object is None:
        return False

    log.info(f"center_on_target {target_object}")
    [obj, [height, width, area]] = target_object
    [left, top, right, bottom] = obj["boundingBox"]

    obj_center_x = left + width / 2
    obj_center_delta = obj_center_x - VIEW_CENTER[0]
    degrees_off = obj_center_delta / PIXELS_PER_DEGREE
    log.info(f"{degrees_off=}")
    if -1 * DEGREES_OFF_THRESHOLD < degrees_off < DEGREES_OFF_THRESHOLD:
        return True

    await rotate_degrees(websocket, obj_center_delta / PIXELS_PER_DEGREE)
    # we don't know if it's centered or not until we go through the
    # outer loop and reacquire, so return False
    return False


async def move_with_target(target_object):
    log.info(f"Moving to target {target_object=}")
    [obj, [height, width, area]] = target_object

    height_diff = height / c.VISION_HEIGHT
    if height_diff < MIN_PERCENT_HEIGHT:
        log.info("moving forward")
    elif height_diff > MAX_PERCENT_HEIGHT:
        log.info("moving backward")

    await asyncio.sleep(0.2)


def distance_to_object(obj):
    """computes the distance to object from the center based on the depth_map"""
    return 42


def compute_dims(recog_obj):
    """computes the area, height and width of the objects bounding box"""
    [left, top, right, bottom] = recog_obj["boundingBox"]
    height = bottom - top
    width = right - left
    return (height, width, height * width)


async def rotate_degrees(websocket, deg):
    [left_throttle, right_throttle] = (
        [ROTATION_THROTTLE, ROTATION_THROTTLE * -1]
        if deg > 0
        else [ROTATION_THROTTLE * -1, ROTATION_THROTTLE]
    )
    await state.send_throttles(websocket, left_throttle, right_throttle)
    await asyncio.sleep(SECONDS_PER_DEGREE * abs(deg))
    await state.send_throttles(websocket, 0, 0)

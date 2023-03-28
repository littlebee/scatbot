from commons import messages, log

state = {
    "mode": 0,
    "status": "peachy",
    "targetAcquired": False,
    "targetBoundingBox": [],
}


async def send_state_update(websocket, updates):
    """Sends the 'behavior' key state"""
    global state
    state.update(updates)
    await messages.send_state_update(websocket, {"behavior": state})


async def send_target_state(websocket, target_acquired, bounding_box):
    await send_state_update(
        websocket,
        {
            "targetAcquired": target_acquired,
            "targetBoundingBox": bounding_box,
        },
    )


async def send_throttles(websocket, left_throttle, right_throttle):
    # we don't keep throttle state herein
    throttle_state = {"throttles": {"left": left_throttle, "right": right_throttle}}
    log.info(f"{throttle_state=}")
    await messages.send_state_update(websocket, throttle_state)

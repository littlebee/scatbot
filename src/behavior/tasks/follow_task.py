import asyncio
import traceback

from commons import log, shared_state

CONFIDENCE_THRESHOLD = 0.5
to_match = ["person", "dog", "cat"]


async def follow_task():
    """follow_task is a coroutine that runs when the follow `behave` mode is selected"""
    log.info("follow_task started")

    # task runs until canceled by ../behavior.py
    while True:
        try:
            recog_objects = [
                [obj, distance_to_object(obj)]
                for obj in shared_state.state["recognition"]
                if obj["classification"] in to_match
                and obj["confidence"] >= CONFIDENCE_THRESHOLD
            ]
            if len(recog_objects) > 0:
                log.info(f"follow_task: targets acquired {recog_objects}")

            await asyncio.sleep(1)

        except Exception as e:
            log.error(f"caught exception in follow_task.py: {e}")
            traceback.print_exc()
            log.info("sleeping for 5 seconds before restarting task")
            await asyncio.sleep(5)


def distance_to_object(obj):
    """computes the distance to object from the center based on the depth_map"""
    return 42

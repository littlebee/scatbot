import time
import threading
import asyncio
import json
import websockets
import traceback
import logging

from commons import constants, messages
from commons.fps_stats import FpsStats

logger = logging.getLogger(__name__)

# This class creates a thread the monitors the camera depth image output
# and publishes it via websockets to central hub


class DepthProvider:
    thread = None
    camera = None
    fps_stats = FpsStats()

    def __init__(self, camera):
        DepthProvider.camera = camera
        if DepthProvider.thread is None:
            DepthProvider.thread = threading.Thread(target=self._thread)
            DepthProvider.thread.start()

    @classmethod
    async def provide_state(cls):
        sample_count = 0
        start_time = time.time()
        cls.fps_stats.start()

        while True:
            try:

                print(f"connecting to hub central at {constants.HUB_URI}")
                async with websockets.connect(constants.HUB_URI) as websocket:
                    await messages.send_identity(websocket, "vision")
                    while True:
                        cls.fps_stats.increment()

                        min_distance, max_distance, section_map = cls._generate_section_map()

                        # TODO : to do this, it also needs to incorporate whether any of the
                        #   section minimums changed
                        # abs(min_distance - last_min_distance) > constants.DEPTH_MAP_CHANGE_TOLERACE:
                        if True:
                            last_min_distance = min_distance
                            message = json.dumps({
                                "type": "updateState",
                                "data": {
                                    "depth_map": {
                                        "min_distance": min_distance,
                                        "max_distance": max_distance,
                                        "last_updated": time.time(),
                                        "section_map": section_map,
                                    }
                                }
                            })
                            await websocket.send(message)

                        await asyncio.sleep(constants.DEPTH_PUBLISH_INTERVAL)
            except:
                traceback.print_exc()

            print('hub central socket disconnected.  Reconnecting in 5 sec...')
            time.sleep(5)

    @classmethod
    def stats(cls):
        return {
            "fps": cls.fps_stats.stats(),
        }

    @classmethod
    def _generate_section_map(cls):
        depth_data = cls.camera.get_depth_data().tolist()

        min_value = 0
        max_value = 0
        target_width = constants.DEPTH_MAP_SECTION_WIDTH
        target_height = constants.DEPTH_MAP_SECTION_HEIGHT

        section_map = [
            [0]*target_width for i in range(target_height)]

        for iy, line in enumerate(depth_data):
            section_y = int(
                iy / (len(depth_data) / target_height))
            for ix, value in enumerate(line):
                section_x = int(
                    ix / (len(line) / target_width))
                value = int(value / 10)
                if value > 0:
                    sec_depth = section_map[section_y][section_x]
                    if sec_depth == 0 or value < sec_depth:
                        section_map[section_y][section_x] = value

                    if min_value == 0 or value < min_value:
                        min_value = value
                    if value > max_value:
                        max_value = value

        return min_value, max_value, section_map

    @ classmethod
    def _thread(cls):
        logger.info('Starting pytorch thread.')
        asyncio.run(cls.provide_state())

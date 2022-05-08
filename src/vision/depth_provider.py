import time
import threading
import asyncio
import json
import websockets
import traceback
import logging

from commons import constants
from commons.fps_stats import FpsStats

logger = logging.getLogger(__name__)

# This class creates a thread the monitors the cammera depth image output
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
                    while True:
                        cls.fps_stats.increment()

                        depth_data = cls.camera.get_depth_data().tolist()

                        min_value = 65535
                        max_value = 0
                        target_width = constants.DEPTH_MAP_SECTION_WIDTH
                        target_height = constants.DEPTH_MAP_SECTION_HEIGHT
                        sectioned_min_map = [
                            [0]*target_width for i in range(target_height)]
                        for iy, line in enumerate(depth_data):
                            section_y = int(
                                iy / (len(depth_data) / target_height))
                            for ix, value in enumerate(line):
                                section_x = int(
                                    ix / (len(line) / target_width))

                                if value > 5 and value < 65535:
                                    sec_depth = sectioned_min_map[section_y][section_x]
                                    if sec_depth == 0 or value < sec_depth:
                                        sectioned_min_map[section_y][section_x] = value

                                    if value < min_value:
                                        min_value = value
                                    if value > max_value:
                                        max_value = value

                        # TODO : only publish if distances have a minimum
                        #    amount of differences
                        if True:  # diff > constants.DEPTHMAP_CHANGE_TOLERANCE:
                            message = json.dumps({
                                "type": "updateState",
                                "data": {
                                    "depth_map": {
                                        "min_distance": min_value,
                                        "max_distance": max_value,
                                        "size": len(depth_data),
                                        "last_updated": time.time(),
                                        "section_min_map": sectioned_min_map
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
    def _thread(cls):
        logger.info('Starting pytorch thread.')
        asyncio.run(cls.provide_state())

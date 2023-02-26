import time
import threading
import asyncio
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
    section_map = [[]]

    def __init__(self, camera):
        DepthProvider.camera = camera
        if DepthProvider.thread is None:
            DepthProvider.thread = threading.Thread(target=self._thread)
            DepthProvider.thread.start()

    @classmethod
    async def provide_state(cls):
        cls.fps_stats.start()

        while True:
            try:
                print(
                    f"depth_provider connecting to hub central at {constants.HUB_URI}"
                )
                async with websockets.connect(constants.HUB_URI) as websocket:
                    await messages.send_identity(websocket, "vision")
                    while True:
                        cls.fps_stats.increment()

                        depth_data = cls.camera.get_depth_data()
                        cls.section_map = depth_data

                        # print(f"got depth_data {depth_data}")

                        await messages.send_state_update(
                            websocket,
                            {
                                "depth_map": {
                                    "last_updated": time.time(),
                                    "section_map": depth_data,
                                }
                            },
                        )

                        await asyncio.sleep(constants.DEPTH_PUBLISH_INTERVAL)
                        # time.sleep(0)
            except:
                traceback.print_exc()

            print("central_hub socket disconnected.  Reconnecting in 5 sec...")
            time.sleep(5)

    @classmethod
    def stats(cls):
        return {
            "fps": cls.fps_stats.stats(),
            "section_map": cls.section_map,
        }

    @classmethod
    def _thread(cls):
        logger.info("Starting depth map thread.")
        asyncio.run(cls.provide_state())

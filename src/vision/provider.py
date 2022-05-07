import time
import json
import asyncio
import traceback
import websockets

import pyrealsense2 as rs
import numpy as np

from commons import constants


async def provide_state():
    sample_count = 0
    start_time = time.time()
    # last_sample = 0
    while True:
        try:
            # Create a context object. This object owns the handles to all connected realsense devices
            pipeline = rs.pipeline()

            # Configure streams
            config = rs.config()
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

            # Start streaming
            pipeline.start(config)

            print(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                while True:
                    frames = pipeline.wait_for_frames()
                    depth_frame = frames.get_depth_frame()
                    depth_array = np.asanyarray(depth_frame.get_data())
                    # last_sample = sample
                    if True:  # diff > constants.COMPASS_CHANGE_TOLERANCE:
                        message = json.dumps({
                            "type": "updateState",
                            "data": {
                                "depth_map": depth_array.to_list(),
                            }
                        })
                        await websocket.send(message)
                    sample_count += 1
                    if sample_count == 50000:
                        elapsed = time.time() - start_time
                        print(
                            f"Got {sample_count} samples in {elapsed} seconds. ({sample_count/elapsed} Hz)")
                        sample_count = 0
                        start_time = time.time()
                    await asyncio.sleep(1)
        except:
            traceback.print_exc()

        print('socket disconnected.  Reconnecting in 5 sec...')
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

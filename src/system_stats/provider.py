import os
import time
import json
import asyncio
import traceback
import websockets
import psutil


from commons import constants, messages


def get_update_message():
    (cpu_temp, *rest) = [
        int(i) / 1000 for i in
        os.popen(
            'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
    ]
    return json.dumps({
        "type": "updateState",
        "data": {
            "system_stats": {
                "cpu_util": psutil.cpu_percent(),
                "cpu_temp": cpu_temp,
                "ram_util": psutil.virtual_memory()[2],
            },
        }
    })


async def provide_state():
    while True:
        try:
            print(f"connecting to {constants.HUB_URI}")
            async with websockets.connect(constants.HUB_URI) as websocket:
                await messages.send_identity(websocket, "system_stats")
                while True:
                    message = get_update_message()
                    await websocket.send(message)
                    await asyncio.sleep(constants.SYSTEM_STATS_SAMPLE_INTERVAL)
        except:
            traceback.print_exc()

        print('socket disconnected.  Reconnecting in 5 sec...')
        time.sleep(5)


def start_provider():
    asyncio.run(provide_state())

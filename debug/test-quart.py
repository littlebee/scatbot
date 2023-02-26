#!/usr/bin/env python3
import logging
import json
import asyncio
from quart import Quart, render_template, websocket
from functools import wraps


logging.basicConfig()


def iseeu_message():
    remoteIp = websocket.remote_address[0]
    return json.dumps(
        {
            "type": "iseeu",
            "data": {
                "ip": remoteIp,
            },
        }
    )


# async def send_message(websocket, message):
#     if websocket and websocket != "all":
#         await websocket.send(message)
#     elif DataStore.SOCKETS:  # asyncio.wait doesn't accept an empty list
#         await asyncio.wait([websocket.send(message) for websocket in DataStore.SOCKETS])


# async def notify_state(websocket="all"):
#     await send_message(websocket, DataStore.serializeGameState())


# async def notify_config(websocket="all"):
#     await send_message(websocket, DataStore.serializeGameConfig())


# # NOTE that there is no "all" option here, need a websocket,
# #  ye shall not ever broadcast this info
# async def notify_iseeu(websocket):
#     if not websocket or websocket == "all":
#         return
#     await send_message(websocket, iseeu_message(websocket))


# async def register(websocket):
#     print(f"got new connection from {websocket.remote_address[0]}")
#     DataStore.SOCKETS.add(websocket)
#     await notify_config(websocket)
#     await notify_state(websocket)
#     await notify_iseeu(websocket)


app = Quart(__name__)

connected_websockets = set()


def collect_websocket(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global connected_websockets
        queue = asyncio.Queue()
        connected_websockets.add(queue)
        try:
            return await func(queue, *args, **kwargs)
        finally:
            connected_websockets.remove(queue)

    return wrapper


async def broadcast(message):
    for queue in connected_websockets:
        await queue.put(message)


@app.route("/")
async def hello():
    return await render_template("index.html")


@app.websocket("/ws")
@collect_websocket
async def ws(queue):
    await websocket.send_json({"hello": "world"})

    while True:
        print("awaiting message")
        data = await queue.get()
        print(f"got message {data}")
        await broadcast(data)

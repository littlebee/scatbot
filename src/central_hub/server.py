#!/usr/bin/env python3

import logging
import json
import asyncio
import websockets

from commons import enums, constants, shared_state


logging.basicConfig()

connected_sockets = set()

# a dictionary of sets containing sockets by top level
# dictionary key in shared_state
subscribers = dict()


def iseeu_message(websocket):
    remoteIp = websocket.remote_address[0]
    return json.dumps({
        "type": "iseeu",
        "data": {
            "ip": remoteIp,
        }
    })


async def send_message(websocket, message):
    if websocket and websocket != "all":
        await websocket.send(message)
    elif connected_sockets:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([websocket.send(message) for websocket in connected_sockets])


async def notify_state(websocket="all"):
    await send_message(websocket, shared_state.serializeState())


async def notify_config(websocket="all"):
    await send_message(websocket, shared_state.serializeConfig())


# NOTE that there is no "all" option here, need a websocket,
#  ye shall not ever broadcast this info
async def notify_iseeu(websocket):
    if not websocket or websocket == "all":
        return
    await send_message(websocket, iseeu_message(websocket))


async def register(websocket):
    print(f"got new connection from {websocket.remote_address[1]}:")
    connected_sockets.add(websocket)


async def unregister(websocket):
    print(f"lost connection {websocket.remote_address[1]}")
    try:
        connected_sockets.remove(websocket)
        for key in subscribers:
            subscribers[key].remove(websocket)
    except:
        pass


async def handleStateRequest(websocket):
    await notify_state(websocket)


async def handleStateUpdate(websocket, message_data):
    global subscribers

    shared_state.update_state_from_message_data(message_data)

    subscribed_sockets = set()
    for key in message_data:
        if key in subscribers:
            print(f"subscribed sockets for {key}: {subscribers[key]}")
            for sub_socket in subscribers[key]:
                subscribed_sockets.add(sub_socket)

    relay_message = json.dumps({
        "type": "stateUpdate",
        "data": message_data
    })
    for socket in subscribed_sockets:
        await send_message(socket, relay_message)


async def handleStateSubscribe(websocket, data):
    global subscribers
    subscription_keys = []
    if data == "*":
        subscription_keys = shared_state.SHARED_STATE.keys()
    else:
        subscription_keys = data

    for key in subscription_keys:
        socket_set = None
        if key in subscribers:
            socket_set = subscribers[key]
        else:
            socket_set = set()
            subscribers[key] = socket_set

        print(f"subscribing {websocket} to {key}")
        socket_set.add(websocket)


async def handleStateUnsubscribe(websocket, data):
    global subscribers
    subscription_keys = []
    if data == "*":
        subscription_keys = subscribers.keys()
    else:
        subscription_keys = data

    for key in subscription_keys:
        if key in subscribers:
            subscribers[key].remove(websocket)


async def handleMessage(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            print(f"{message} from {websocket.remote_address[1]}")
            jsonData = json.loads(message)
            messageType = jsonData.get("type")
            messageData = jsonData.get('data')

            # {type: "state"}
            if messageType == "getState":
                await handleStateRequest(websocket)
            # {type: "updateState" data: { new state }}
            elif messageType == "updateState":
                await handleStateUpdate(websocket, messageData)
            # {type: "subscribeState", data: [state_keys] or "*"
            elif messageType == "subscribeState":
                await handleStateSubscribe(websocket, messageData)
            # {type: "unsubscribeState", data: [state_keys] or "*"
            elif messageType == "unsubscribeState":
                await handleStateUnsubscribe(websocket, messageData)
            else:
                logging.error("received unsupported message: %s", messageType)
    finally:
        await unregister(websocket)


print(f"Starting server on port {constants.HUB_PORT}")
start_server = websockets.serve(handleMessage, port=constants.HUB_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

import os
import json

LOG_ALL_MESSAGES = os.getenv('LOG_ALL_MESSAGES') or False


async def send_message(websocket, message):
    json_message = json.dumps(message)
    if LOG_ALL_MESSAGES:
        print(f"{json_message} to {websocket.remote_address[1]}")
    await websocket.send(json_message)


async def send_identity(websocket, name):
    await send_message(websocket, {
        "type": "identity",
        "data": name,
    })


# subscriptionNames should be an array or "*"
async def send_subscribe(websocket, subscriptionNames):
    await send_message(websocket, {
        "type": "subscribeState",
        "data": subscriptionNames,
    })


async def send_get_state(websocket):
    await send_message(websocket, {
        "type": "getState",
    })


async def send_state_update(websocket, stateData):
    await send_message(websocket, {
        "type": "updateState",
        "data": stateData,
    })

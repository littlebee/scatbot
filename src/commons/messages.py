
import json


async def send_identity(websocket, name):
    await websocket.send(json.dumps({
        "type": "identity",
        "data": name,
    }))


# subscriptionNames should be an array or "*"
async def send_subscribe(websocket, subscriptionNames):
    await websocket.send(json.dumps({
        "type": "subscribeState",
        "data": subscriptionNames,
    }))

# subscriptionNames should be an array or "*"


async def send_state_update(websocket, stateData):
    await websocket.send(json.dumps({
        "type": "updateState",
        "data": stateData,
    }))

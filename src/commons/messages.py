
import json


async def send_identity(websocket, name):
    await websocket.send(json.dumps({
        "type": "identity",
        "data": name,
    }))

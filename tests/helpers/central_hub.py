import json
import os
import time

# Note this is actually the websocket_client and not the websockets lib.
# websocket_client provides a way of synchronously sending and receiving
# ws messages.  See: https://pypi.org/project/websocket-client/
import websocket

websocket.enableTrace(True)

CENTRAL_HUB_TEST_PORT = 9069
DEFAULT_TIMEOUT = 5


def start():
    """starts central hub as a detached process using same start script used to start on the bot"""
    cmd = f"LOG_ALL_MESSAGES=1 HUB_PORT={CENTRAL_HUB_TEST_PORT} poetry run ./start.sh central_hub"
    exit_code = os.system(cmd)
    assert exit_code == 0
    time.sleep(1)


def stop():
    """stops central hub"""
    exit_code = os.system("./stop.sh central_hub")
    assert exit_code == 0


def connect():
    """connect to central hub and return a websocket (websocket-client lib)"""
    ws = websocket.create_connection(f"ws://localhost:{CENTRAL_HUB_TEST_PORT}/ws")
    ws.settimeout(DEFAULT_TIMEOUT)
    return ws


def send(ws, dict):
    """send dictionary as json to central hub"""
    return ws.send(json.dumps(dict))


def send_state_update(ws, dict):
    send(
        ws,
        {
            "type": "updateState",
            "data": dict,
        },
    )


def recv(ws):
    return json.loads(ws.recv())


def has_received_data(ws):
    # note zero doesn't work here because it causes it creates a non blocking socket
    # plus we need to give central hub chance to reply for test purposes
    ws.settimeout(0.1)
    try:
        return recv(ws)
    except websocket._exceptions.WebSocketTimeoutException:
        return False
    finally:
        ws.settimeout(DEFAULT_TIMEOUT)


def has_received_state_update(ws, key, value):
    stateUpdate = recv(ws)
    return stateUpdate["type"] == "stateUpdate" and stateUpdate["data"][key] == value

import helpers.central_hub as hub

ANSWER = 42


def setup_module():
    hub.start()


def teardown_module():
    hub.stop()


class TestCentralHub:
    def test_connect_identify(self):
        ws = hub.connect()
        hub.send(ws, {"type": "identity", "data": "test_system"})
        response = hub.recv(ws)
        ws.close()

        assert response["type"] == "iseeu"

    def test_state(self):
        ws = hub.connect()

        hub.send(ws, {"type": "getState"})
        initial_state = hub.recv(ws)
        print(f"{initial_state=}")
        assert initial_state["data"]["compass"] != ANSWER

        hub.send(
            ws,
            {
                "type": "updateState",
                "data": {
                    "compass": ANSWER,
                },
            },
        )
        hub.send(ws, {"type": "getState"})
        updated_state = hub.recv(ws)
        assert updated_state["data"]["compass"] == ANSWER

        ws.close()

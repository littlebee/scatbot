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

        hub.send_state_update(ws, {"compass": ANSWER})
        hub.send(ws, {"type": "getState"})
        updated_state = hub.recv(ws)
        assert updated_state["data"]["compass"] == ANSWER

        ws.close()

    def test_pubsub(self):
        ws1 = hub.connect()
        hub.send_subscribe(ws1, ["compass", "behavior"])
        # should not have received anything in response to subscribe
        assert not hub.has_received_data(ws1)

        ws2 = hub.connect()
        hub.send_subscribe(ws2, ["behavior"])

        # second client sends a compass update
        hub.send_state_update(ws2, {"compass": ANSWER})
        # the second client should not receive a compass update because it is not subscribed to "compass"
        assert not hub.has_received_data(ws2)
        # first client has subscribed to compass updates and should recv a message
        assert hub.has_received_state_update(ws1, "compass", ANSWER)

        # second client sends a behavior update which both clients are subscribed
        hub.send_state_update(ws2, {"behavior": ANSWER})
        # first client has subscribed to behavior updates and should recv a message
        assert hub.has_received_state_update(ws1, "behavior", ANSWER)
        # second client has also subscribed to behavior updates and should recv a message
        assert hub.has_received_state_update(ws2, "behavior", ANSWER)

        # first client sends a behavior update which both clients are subscribed
        hub.send_state_update(ws1, {"behavior": ANSWER + 5})
        # first client has subscribed to behavior updates and should recv a message
        assert hub.has_received_state_update(ws1, "behavior", ANSWER + 5)
        # second client has also subscribed to behavior updates and should recv a message
        assert hub.has_received_state_update(ws2, "behavior", ANSWER + 5)

        # first client sends a feeder update which neither clients are subscribed
        hub.send_state_update(ws1, {"feeder": ANSWER})
        assert not hub.has_received_data(ws1)
        assert not hub.has_received_data(ws1)

        # after all of the above, our state should reflect all changes
        hub.send(ws1, {"type": "getState"})
        updated_state = hub.recv(ws1)
        assert updated_state["data"]["compass"] == ANSWER
        assert updated_state["data"]["behavior"] == ANSWER + 5
        assert updated_state["data"]["feeder"] == ANSWER

        ws1.close()
        ws2.close()

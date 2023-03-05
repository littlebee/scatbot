import helpers.central_hub as hub
import helpers.behavior as behavior

from commons.constants import BEHAVIORS


def setup_module():
    hub.start()
    behavior.start()


def teardown_module():
    behavior.stop()
    hub.stop()


class TestBehavior:
    def test_change_behavior(self):
        ws = hub.connect()
        hub.send_subscribe(ws, ["behavior"])

        # `behave` key should initially be BEHAVIORS.RC.value
        hub.send(ws, {"type": "getState"})
        initial_state = hub.recv(ws)
        assert initial_state["data"]["behave"] != BEHAVIORS.FOLLOW.value

        # changing the set behavior mode ('behave') should update the `behavior` key
        hub.send_state_update(ws, {"behave": BEHAVIORS.FOLLOW.value})
        hub_message = hub.recv(ws)
        assert hub_message["type"] == "stateUpdate"
        assert hub_message["data"]["behavior"]["mode"] == BEHAVIORS.FOLLOW.value

        # changing the set behavior mode ('behave') back to RC should also update the `behavior` key
        hub.send_state_update(ws, {"behave": BEHAVIORS.RC.value})
        hub_message = hub.recv(ws)
        assert hub_message["type"] == "stateUpdate"
        assert hub_message["data"]["behavior"]["mode"] == BEHAVIORS.RC.value

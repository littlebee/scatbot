import "react";
import { createState } from "@hookstate/core";

export const HubState = createState({
  hubConnStatus: "offline",
  // which behavior - RC, hide $ seek, follow
  behavior: 0,
  // feedback about what behavior is doing
  behavior_status: "offline",

  // heading
  compass: 0,

  // depth map - array of mm distance from camera per pixel
  depth_map: [],

  // recognized objects from pytorch
  inference: [
    // this is a array of
    //  {
    //     "classificaton": "dog",
    //     "bounding_box": [0, 0, 0, 0],
    //     "confidence": 90
    //  }
  ],
});
// setInterval(() => HubState.hubConnStatus.set((p) => p + 1), 3000);

const HUB_HOST =
  !process.env.NODE_ENV || process.env.NODE_ENV === "development"
    ? "scatbot.local:5000"
    : `${window.location.hostname}:5000`;

export let webSocket = null;

connectToHub(HubState);

// not exported, should only be called from connectToHub
function setHubConnStatus(newStatus) {
  console.log("setting conn status", newStatus);
  HubState.hubConnStatus.set(newStatus);
}

export function connectToHub(state) {
  try {
    const hubUrl = `ws://${HUB_HOST}/ws`;
    setHubConnStatus("connecting");
    console.log("connecting to central-hub at ${hubUrl}");

    webSocket = new WebSocket(hubUrl);

    webSocket.addEventListener("open", function (event) {
      try {
        webSocket.send(JSON.stringify({ type: "getState" }));
        webSocket.send(JSON.stringify({ type: "subscribeState", data: "*" }));
        setHubConnStatus("online");
      } catch (e) {
        onConnError(state, e);
      }
    });

    webSocket.addEventListener("error", function (event) {
      console.error("got error from central-hub socket", event);
    });

    webSocket.addEventListener("close", function (event) {
      onConnError(state, event);
    });

    webSocket.addEventListener("message", function (event) {
      console.log("got message from central-hub", event.data);
      const message = JSON.parse(event.data);
      if (message.type == "state" || message.type == "stateUpdate")
        updateStateFromCentralHub(message.data);
    });
  } catch (e) {
    onConnError(state, e);
  }
}

function delayedConnectToHub(state) {
  setTimeout(() => {
    if (state.hubConnStatus.get() === "offline") {
      connectToHub(state);
    }
  }, 5000);
}

function onConnError(state, e) {
  console.error(
    "got close message from central-hub socket. will attempt to reconnnect in 5 seconds",
    e
  );
  setHubConnStatus("offline");
  delayedConnectToHub(state);
}

function updateStateFromCentralHub(hubData) {
  for (const [key, value] of Object.entries(hubData)) {
    console.log("got hub state update", key, value);
    HubState[key].set(value);
  }
}

import "react";
import { createState } from "@hookstate/core";

const urlParams = new URLSearchParams(window.location.search);
const debugThings = urlParams.get("debug")?.split(",") || [];
const logMesssages = debugThings.indexOf("messages") >= 0;

let hubStatePromises = [];

export const HubState = createState({
  // this is UI only
  hubConnStatus: "offline",

  // the keys below are shared from central hub.  See shared_state.py
  battery: {
    voltage: 0,
    current: 0,
  },

  // which behavior - RC, hide $ seek, follow
  behavior: 0,

  // heading
  compass: 0,

  // depth map - array of mm distance from camera per pixel
  depth_map: {
    min_distance: 0,
    max_distance: 0,
    section_map: [],
  },

  // recognized objects from pytorch
  inference: [
    // this is a array of
    //  {
    //     "classificaton": "dog",
    //     "bounding_box": [0, 0, 0, 0],
    //     "confidence": 90
    //  }
  ],

  hub_stats: {
    state_updates_recv: 0,
  },

  // This is separate from throttles which is the requested throttles.
  // This is what motor_control subsystem says the actual throttles are.
  motors: {
    left: 0,
    right: 0,
    feeder: 0,
  },

  system_stats: {
    cpu_util: 0,
    cpu_temp: 0,
    ram_util: 0,
  },

  subsystem_stats: {
    central_hub: {
      online: 0,
    },
    compass: {
      online: 0,
    },
    motor_control: {
      online: 0,
    },
    onboard_ui: {
      online: 0,
    },
    system_stats: {
      online: 0,
    },
    vision: {
      online: 0,
    },
  },

  throttles: {
    left: 0,
    right: 0,
  },
});
// setInterval(() => HubState.hubConnStatus.set((p) => p + 1), 3000);

export const HUB_HOST =
  !process.env.NODE_ENV || process.env.NODE_ENV === "development"
    ? "scatbot.local:5000"
    : `${window.location.hostname}:5000`;

export const HUB_URL = `ws://${HUB_HOST}/ws`;

export let webSocket = null;

export function connectToHub(state = HubState) {
  try {
    setHubConnStatus("connecting");
    console.log(`connecting to central-hub at ${HUB_URL}`);

    webSocket = new WebSocket(HUB_URL);

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
      log("got message from central-hub", event.data);
      const message = JSON.parse(event.data);
      if (message.type === "state" && hubStatePromises.length > 0) {
        hubStatePromises.forEach((p) => p(message.data));
        hubStatePromises = [];
      } else if (message.type === "state" || message.type === "stateUpdate") {
        updateStateFromCentralHub(message.data);
      }
    });
  } catch (e) {
    onConnError(state, e);
  }
}

export function getStateFromCentralHub() {
  const statePromise = new Promise((resolve) => hubStatePromises.push(resolve));
  webSocket.send(JSON.stringify({ type: "getState" }));
  return statePromise;
}

export function updateSharedState(newState) {
  webSocket.send(JSON.stringify({ type: "updateState", data: newState }));
}

export function sendThrottles(leftThrottle, rightThrottle) {
  console.log("sending throttles", {
    leftThrottle,
    rightThrottle,
  });

  webSocket.send(
    JSON.stringify({
      type: "updateState",
      data: {
        throttles: {
          left: leftThrottle,
          right: rightThrottle,
        },
      },
    })
  );
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

// not exported, should only be called from connectToHub
function setHubConnStatus(newStatus) {
  log("setting conn status", newStatus);
  HubState.hubConnStatus.set(newStatus);
}

function updateStateFromCentralHub(hubData) {
  for (const [key, value] of Object.entries(hubData)) {
    log("got hub state update", key, value);
    // TODO : unless we merge the state with incoming
    // state for any top level key must be whole
    HubState[key].set(value);
  }
}

function log(...args) {
  if (logMesssages) {
    console.log(...args);
  }
}

# Scatbot

A robot to follow my dog around and give her treats

<img src="https://github.com/littlebee/Scatbot/blob/fdfa67ec1966cedb2e5a322f2bc2d7778dd695b0/docs/img/scatbot-pi-design.png"
     alt="design image"
     style="float: right; margin-right: 10px; width: 400px;" />

I originally got the idea for Scatbot watching my dog interact with the Roomba. She seemed disappointed and frustrated that El Roomba just went about his business as if she wasn't sitting right there with the ball the robot had just pushed out from under the couch. How rude.

Scatbot is designed to be about the same height as a Roomba (< 100mm) so that it can fit under most of my furniture.

The idea is that it will be R/C or autonomous with several autonomous modes like "Follow" or "Hide and Seek".

Originally I started designing, and even built an alpha-1 prototype, around the Nvidia Jetson Nano, but a couple of things doomed that design. Space! is so important and the Nano is not very small when you add on it's big heat sink and fan. Also the torture of getting all of the 3rd party software (tensor flow, opencv, adafruit motorkit, ...) working together was a brutal dungeon craw.

It runs on a Raspberry PI 4b w/4GB. The [Adafruit Braincraft hat](https://www.adafruit.com/product/4374) provides the onboard-ui, audio amplifier and a few LEDs that are used for expressive behaviors.

## See also

Spreadsheet of parts:
https://docs.google.com/spreadsheets/d/1Sh4O05_kYhsgo-QO83rhAAbxgSdKjL1iUw-a6iWCc7w/edit?usp=sharing

Fusion 360 designs:
https://ymail2984.autodesk360.com/g/shares/SH35dfcQT936092f0e436a5991538bbd4822

## How it works

<img src="https://github.com/littlebee/scatbot/blob/c2800de8906b14173201d16030e8d390157eb641/docs/img/scatbot-systems-diagram.png"
     alt="system diagram"
     style="float: right; margin-right: 10px; width: 400px;" />

Scatbot has several sub-systems that interact to provide data from the underlying system, sensors, cameras and object detection. There are also sub-systems that consume that information and provide motor control and autonomous behaviors. All of the sub-systems of Scatbot are individual python processes and can be viewed via an ssh shell using the `ps` command:

```
$ ps -ef | grep python
root         574       1  5 Feb24 ?        05:12:45 python3 src/start_central_hub.py
root         665       1  0 Feb24 ?        00:58:39 python3 src/start_compass.py
root         668       1  0 Feb24 ?        00:00:36 python3 src/start_motor_control.py
root         706       1  8 Feb24 ?        08:43:46 python3 src/start_onboard_ui.py
root         718       1  1 Feb24 ?        01:17:46 python3 src/start_system_stats.py
root         792       1  0 Feb24 ?        00:01:08 python3 src/start_behavior.py
root         792       1  0 Feb24 ?        00:01:08 python3 src/start_web_server.py
root         828       1 37 Feb24 ?        1-13:21:09 python3 src/start_vision_realsense.py
root     1380847       1 94 Feb26 ?        1-15:47:19 python3 src/start_vision.py
```

All of the sub-systems provide or subscribe to data via `central-hub`.

### central-hub

`central-hub` provides an ultra light weight pub/sub service. It provides a web socket interface on port 5000 that the other subsystems connect to, identify themselves, request the full state, subscribe to state keys and provide state updates via messages to the socket.

`central-hub` maintains the authoritative source of state in an in-memory dictionary. See: https://github.com/littlebee/Scatbot/blob/main/debug/commons/shared_state.py#L4 for the default state values.

Sub-systems can send a `subscribeState` with top level keys of the shared state and receive `stateUpdate` messages whenever something under one of those keys change.

### Message protocol and API

All messages to and from `central-hub` are in JSON and have the format:

```json
{
  "type": "string",
  "data": {}
}
```

Where `data` is optional and specific to the type of message. The following messages are supported by `central-hub`:

#### getState

example json:

```json
{
  "type": "getState"
}
```

Causes `central-hub` to send the full state via message type = "state" to the requesting client socket.

### identity

example json:

```json
{
  "type": "identity",
  "data": "My subsystem name"
}
```

Causes `central-hub` to update `subsystems_stats` key of the shared state and send an "iseeu" message back to client socket with the IP address that it sees the client.

### subscribeState

example json:

```json
{
  "type": "subscribeState",
  "data": ["system_stats", "compass"]
}
```

Causes `central-hub` to add the client socket to the subscribers for each of the state keys provided. Client will start receiving "stateUpdate" messages when those keys are changed. The client may also send `"data": "*"` which will subscribe it to all keys like the web UI does.

### updateState

example json:

```json
{
  "type": "updateState",
  "data": {
    "compass": 127.4,
    "throttles": {
      "left": 0,
      "right": 0
    }
  }
}
```

This message causes `central-hub` merge the receive state and the shared state and send `stateUpdate` messages to any subscribers. Note that the message sent **by clients** (type: "updateState") is a different type than the message **sent to clients** (type: "stateUpdate").

As the example above shows, it is possible to update multiple state keys at once, but most subsystems only ever update one top level key.

The data received must be the **full data for that key**. `central-hub` will replace that top level key with the data received.

### more

See the [central hub switch source](https://github.com/littlebee/Scatbot/blob/6c179c63231e4363c791b09ce4e7f3c8b00bc4e3/src/central_hub/server.py#L180) for more information on supported message types.

## compass subsystem

Provides keys: `compass`
Subscribes to keys: `none`

## motor_control subsystem

Provides keys: `motors`
Subscribes to keys: `throttles`, `feeder`

## onboard_ui subsystem

Provides keys: `none`
Subscribes to keys: `system_stats`, `battery`

`onboard_ui` provides the information displayed on Scatbot's onboard LCD (Adafruit Braincraft Hat). Futurue updates will include the ability to set the `behavior` key.

## system_stats subsystem

Provides keys: `system_stats`
Subscribes to keys: `none`

Provides hardware info like percent cpu utilization (`cpu_util`) and temperature (`cpu_temp`) and percent memory utilization (`ram_util`)

## behavior subsystem

Provides keys: `none`
Subscribes to keys: `behavior, *`

The behavior key in shared state represents which autonomous mode or remote control mode that Scatbot is configured. It is changed manually from the `webapp` or from the `onboard_ui`. Different autonomous behaviors need keys from shared state.

## web_server subsystem and webapp

The `web_server` subsystem is a simple flask web server that serves up the React webapp from src/webapp/build on port 80. The `webapp` runs in the user's browser and connects to `central_hub` websocket remotely. `webapp` provides a human user with UI that allows remote motor control + remote real time viewing. The user can also click on the hub state button in the upper left to view the full shared state.

Provides keys: `behavior`, `throttles`, `feeder`
Subscribes to keys: `*`

Additionally, to stream RGB and depth video, `webapp` connects directly to a flask endpoint on the `vision` and `vision_realsense` subsystem.

For rgb video stream, Scatbot connects an img element to:
http://scatbot.local:5001/video_feed?rand=0

For depth video display:
http://scatbot.local:5002/depth_feed?rand=0.6099424588409756

## vision subsystem

Provides keys: `recognition`
Subscribes to keys: `none`

In addition to providing the the `recognition` key which has information about what recognized objects are in Scatbot's view, the `vision` subsystem also provides a flask endpoint (/video_feed) on port 5001 for the clients to stream RGB video using a multipart jpg format compatible with any HTML img tag.

## vision_realsense subsystem

Provides keys: `depth_map`
Subscribes to keys: `none`

The `vision_realsense` subsystem is specific to the Intel Realsense 435i depth camera. The `depth_map.section_map` provided to `central_hub` is a decimated 5x5 grid of min distances in decimeters. The full resolution (640x480) depth data is also provided via a dedicated flask endpoint (/depth_feed) on port 5002 for the clients to stream RGB video using a multipart jpg format compatible with any HTML img tag.

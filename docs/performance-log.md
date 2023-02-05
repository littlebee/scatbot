# Scatbot Performance Log

Performance is measured on the metrics below with all subsystems running.

Metrics measured:

- **stream fps** - this is the max number of frames per second that the vision subsystem can stream live video at 640x480 to a client. For the remote control mode, 30 fps is the minimum; much lower and lag makes it difficult to control the bot.
- **recog fps** - this is the max number of frames of recognition or object detection that the vision subsystem can can publish to central_hub. For the follow dog and other behaviors, object tracking is used to find my furry friend and follow her around. The faster **recog fps**, the less likely we are to lose the target and have to reacquire.
- **depth fps** - this is max number of frames per second that the vision_realsense subsystem can produced a decimated depth map of the forward field of view. The realsense camera produces a 640x480 array of decimeter measurements that gets reduced (decimated) down to a 5x5 array of min measurements for each of the 25 sections. The speed of depth detection impacts how fast Scatbot can detect a hiding spot when using the hide and seek behavior. The Realsense D435i camera used on Scatbot is unfortunately bad at close in object and objects inside 17cm are practically invisible. Given that, **the depth camera is not used for collision avoidance** which would demand a depth fps of at least 20.
- **cpu** - is a measure of the average cpu utilization when in remote control mode. CPU available is used and needed for all of the autonomous modes.

FPS metrics are measured and recorded from the /stats pages produced by the vision (http://scatbot.local:5001/stats) and vision_realsense (http://scatbot.local:5002/stats) subsystems. The `capture.floatingFps` of the vision subsystem json is used to report the **stream_fps** metric.

CPU metric is recorded from average CPU % displayed on the Scatbot onboard UI.

## 20230205

Raspberry Pi 4b (4GB) with vision and depth

### Current state of performance

stream fps: 27
recog fps: 20
depth fps: 8
cpu: 43%

### Notes

After much experimentation, I was able to identify and implement the following performance improvement improvements:

- Use findings from [Scatbot AI perf shootout](https://github.com/littlebee/scatbot-edge-ai-shootout). Which is to say, use tflite + coral USB TPU with models from coral.

- We still need a second camera for vision and only use realsense camera for depth. I experimented with doing both recognition and depth in the same Python process, but it did not go well. The threading in python dragged fps down to under 8 fps on all three metrics when not using coral tpu and under 4 fps when using the tpu.

- Intel realsense 435i is negatively impacted by the Coral TPU. I think maybe this has do to with USB bus contention. If the vision subsystem is not running or is not using the Coral TPU, depth map generation with decimation runs at almost 30 fps, but more cpu is needed by tflite. There is not much I can do here except trade depth fps for stream & recog fps and less cpu. I can live with 8 fps of decimated depth data.

### src/start_vision.py (with Coral TPU)

stream fps: 27
recog fps: 20
depth fps: 8
cpu: 43%

### DISABLE_CORAL_TPU=1 src/start_vision.py

stream fps: 12
recog fps: 4.3
depth fps: 29.25
cpu: 90%

- Decimation function optimizations! Decimation is the reduction of the 640x480 depth measurements down to a 5x5 subsection of minimums excluding zeros.

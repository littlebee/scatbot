import React, { useEffect } from "react";
import { useState } from "@hookstate/core";

import * as c from "./constants";
import { HubState } from "./hub-state";
import { VideoFeed } from "./VideoFeed";
import { VideoControls } from "./VideoControls";

import "./lcars.css";
import "./App.css";

function App() {
  const hubState = useState(HubState);
  const whichVideo = useState(c.RGB_VIDEO);

  return (
    <div>
      <div className="wrap">
        <div className="left-frame-top"></div>

        <div className="right-frame-top">
          <div className="title">
            <h1>scatbot</h1>
            {/* central hub status: {sharedState.hubConnectionStatus} */}
            <div> hub status: {hubState.hubConnStatus.get()}</div>
            <div> compass: {hubState.compass.get()}</div>
          </div>
          <div className="top-corner-bg">
            <div className="top-corner"></div>
          </div>
          <div className="bar-panel">
            <div className="bar-1"></div>
            <div className="bar-2"></div>
            <div className="bar-3"></div>
            <div className="bar-4">
              <div className="bar-4-inside"></div>
            </div>
            <div className="bar-5"></div>
          </div>
        </div>
      </div>
      <div className="wrap">
        <div className="left-frame" id="gap">
          <div className="sidebar-buttons">
            <a href="/">Remote Control</a>
            <a href="/">Hide & Seek</a>
            <a href="/">Follow</a>
          </div>
        </div>
        <div className="right-frame">
          <div className="bar-panel">
            <div className="bar-6"></div>
            <div className="bar-7"></div>
            <div className="bar-8"></div>
            <div className="bar-9">
              <div className="bar-9-inside"></div>
            </div>
            <div className="bar-10"></div>
          </div>
          <div className="corner-bg">
            <div className="corner"></div>
          </div>
          <div className="content">
            <VideoControls
              whichVideo={whichVideo.get()}
              onSelect={whichVideo.set}
            />
            <VideoFeed whichVideo={whichVideo.get()} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

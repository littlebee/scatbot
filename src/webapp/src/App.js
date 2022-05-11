import React, { useEffect } from "react";
import { useState } from "@hookstate/core";

import * as c from "./constants";
import { HubState } from "./hub-state";

import { Header } from "./Header";
import { VideoFeed } from "./VideoFeed";
import { VideoSelector } from "./VideoSelector";

import "./lcars.css";
import "./App.css";

function App() {
  const hubState = useState(HubState);
  const whichVideo = useState(c.RGB_VIDEO);

  return (
    <div>
      <Header hubState={hubState} />
      <div className="wrap">
        <div className="left-frame" id="gap">
          <div className="sidebar-buttons">
            <a href="/">Remote Control</a>
          </div>
          <div className="sidebar-buttons">
            <a href="/">Give Treat</a>
          </div>
          <div className="panel-3"></div>
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
            <VideoSelector
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

import React, { useState } from "react";

import * as c from "./constants";
import { VideoFeed } from "./VideoFeed";
import { VideoControls } from "./VideoControls";

import "./lcars.css";
import "./App.css";

function App() {
  const [whichVideo, setWhichVideo] = useState(c.RGB_VIDEO);

  return (
    <div>
      <div className="wrap">
        <div className="left-frame-top"></div>

        <div className="right-frame-top">
          <div className="title">
            <h1>scatbot</h1>
          </div>
          <div class="top-corner-bg">
            <div class="top-corner"></div>
          </div>
          <div class="bar-panel">
            <div class="bar-1"></div>
            <div class="bar-2"></div>
            <div class="bar-3"></div>
            <div class="bar-4">
              <div class="bar-4-inside"></div>
            </div>
            <div class="bar-5"></div>
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
          <div class="bar-panel">
            <div class="bar-6"></div>
            <div class="bar-7"></div>
            <div class="bar-8"></div>
            <div class="bar-9">
              <div class="bar-9-inside"></div>
            </div>
            <div class="bar-10"></div>
          </div>
          <div class="corner-bg">
            <div class="corner"></div>
          </div>
          <div className="content">
            <VideoControls whichVideo={whichVideo} onSelect={setWhichVideo} />
            <VideoFeed whichVideo={whichVideo} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

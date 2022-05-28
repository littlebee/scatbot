import React, { useState, useEffect } from "react";

import * as c from "./constants";
import {
  DEFAULT_HUB_STATE,
  connectToHub,
  addHubStateUpdatedListener,
  removeHubStateUpdatedListener,
} from "./hub-state";

import { Header } from "./Header";
import { VideoFeed } from "./VideoFeed";
import { VideoSelector } from "./VideoSelector";
import { OverlaySelector } from "./OverlaySelector";
import { HubStateDialog } from "./HubStateDialog";
import { Thumbstick } from "./Thumbstick";

import "./lcars.css";
import "./App.css";

function App() {
  const [hubState, setHubState] = useState(DEFAULT_HUB_STATE);
  const [whichVideo, setWhichVideo] = useState(c.RGB_VIDEO);
  const [whichOverlays, setWhichOverlays] = useState([]);
  const [isHubStateDialogOpen, setIsHubStateDialogOpen] = useState(false);

  useEffect(() => {
    addHubStateUpdatedListener(handleHubStateUpdated);
    connectToHub();

    return () => removeHubStateUpdatedListener(handleHubStateUpdated);
  }, []);

  const handleHubStateUpdated = (newState) => {
    setHubState({ ...newState });
  };

  const handleOverlaySelected = (whichOverlay) => {
    const newOverlays = [...whichOverlays];
    const indexOfOverlayClicked = newOverlays.indexOf(whichOverlay);

    if (indexOfOverlayClicked >= 0) {
      newOverlays.splice(indexOfOverlayClicked, 1);
    } else {
      newOverlays.push(whichOverlay);
    }
    setWhichOverlays(newOverlays);
  };

  return (
    <div>
      <Header
        hubState={hubState}
        isHubStateDialogOpen={isHubStateDialogOpen}
        onHubStateDialogOpen={() => setIsHubStateDialogOpen(true)}
      />
      <div className="wrap">
        <div className="left-frame" id="gap">
          <div className="sidebar-buttons">
            <a>Remote Control</a>
          </div>
          <div className="sidebar-buttons">
            <a>Give Treat</a>
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
            <VideoSelector whichVideo={whichVideo} onSelect={setWhichVideo} />
            <VideoFeed whichVideo={whichVideo} />
            <OverlaySelector
              whichOverlays={whichOverlays}
              onSelect={handleOverlaySelected}
            />
          </div>
        </div>
      </div>
      <Thumbstick />
      <HubStateDialog
        hubState={hubState}
        isOpen={isHubStateDialogOpen}
        onClose={() => setIsHubStateDialogOpen(false)}
      />
    </div>
  );
}

export default App;

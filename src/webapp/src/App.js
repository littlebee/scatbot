import React, { useState, useEffect } from "react";

import * as c from "./constants";
import {
  DEFAULT_HUB_STATE,
  connectToHub,
  addHubStateUpdatedListener,
  removeHubStateUpdatedListener,
  giveTreat,
} from "./hub-state";

import { Header } from "./Header";
import { VideoFeed } from "./VideoFeed";
import { VideoSelector } from "./VideoSelector";
import { Overlays } from "./Overlays";
import { OverlaySelector } from "./OverlaySelector";
import { HubStateDialog } from "./HubStateDialog";
import { Hazards } from "./Hazards";
import { Thumbstick } from "./Thumbstick";
import { BehaviorSelector } from "./BehaviorSelector";

import "./lcars.css";
import "./App.css";

function App() {
  const [hubState, setHubState] = useState(DEFAULT_HUB_STATE);
  const [whichVideo, setWhichVideo] = useState(c.RGB_VIDEO);
  const [whichOverlays, setWhichOverlays] = useState([]);
  const [filterConfidence, setFilterConfidence] = useState(0.5);
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

  const handleGiveTreatClick = (e) => {
    e.preventDefault();
    giveTreat();
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
          <BehaviorSelector hubState={hubState} />
          <div className="sidebar-buttons">
            <a onClick={handleGiveTreatClick}>Give Treat</a>
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
            <Overlays
              whichOverlays={whichOverlays}
              hubState={hubState}
              filterConfidence={filterConfidence}
            >
              <VideoFeed whichVideo={whichVideo} />
            </Overlays>
            <OverlaySelector
              whichOverlays={whichOverlays}
              filterConfidence={filterConfidence}
              onSelect={handleOverlaySelected}
              onFilterConfidence={setFilterConfidence}
            />
          </div>
        </div>
      </div>
      <Hazards hubState={hubState} />
      {hubState.behavior.mode === 0 && <Thumbstick />}
      <HubStateDialog
        hubState={hubState}
        isOpen={isHubStateDialogOpen}
        onClose={() => setIsHubStateDialogOpen(false)}
      />
    </div>
  );
}

export default App;

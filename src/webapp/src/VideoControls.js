import React from "react";

import * as c from "./constants";

export function VideoControls({ whichVideo, onSelect }) {
  let rgbButtonClass = "button";
  let depthButtonClass = "button";
  switch (whichVideo) {
    case c.RGB_VIDEO:
      rgbButtonClass += " selected";
      break;
    case c.DEPTH_VIDEO:
      depthButtonClass += " selected";
      break;
  }

  return (
    <div className="buttons video-controls">
      <div className={rgbButtonClass} onClick={() => onSelect(c.RGB_VIDEO)}>
        <a>RGB Video</a>
      </div>
      <div className={depthButtonClass} onClick={() => onSelect(c.DEPTH_VIDEO)}>
        <a>Depth Video</a>
      </div>
    </div>
  );
}

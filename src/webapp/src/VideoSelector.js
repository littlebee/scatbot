import React from "react";

import * as c from "./constants";
import st from "./VideoSelector.module.css";

export function VideoSelector({ whichVideo, onSelect }) {
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
    <div className={`buttons ${st.videoSelector}`}>
      <div className={rgbButtonClass} onClick={() => onSelect(c.RGB_VIDEO)}>
        <a>RGB Video</a>
      </div>
      <div className={depthButtonClass} onClick={() => onSelect(c.DEPTH_VIDEO)}>
        <a>Depth Video</a>
      </div>
    </div>
  );
}

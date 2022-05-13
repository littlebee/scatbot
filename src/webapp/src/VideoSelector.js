import React from "react";

import * as c from "./constants";
import { Button } from "./components/Button";
import st from "./VideoSelector.module.css";

export function VideoSelector({ whichVideo, onSelect }) {
  return (
    <div className={`buttons ${st.videoSelector}`}>
      <Button
        isSelected={whichVideo === c.RGB_VIDEO}
        onClick={() => onSelect(c.RGB_VIDEO)}
      >
        RGB Video
      </Button>
      <Button
        isSelected={whichVideo === c.DEPTH_VIDEO}
        onClick={() => onSelect(c.DEPTH_VIDEO)}
      >
        Depth Video
      </Button>
    </div>
  );
}

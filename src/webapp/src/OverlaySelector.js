import React from "react";

import * as c from "./constants";
import { Button } from "./components/Button";

import st from "./VideoSelector.module.css";

export function OverlaySelector({ whichOverlays, onSelect }) {
  const isSelected = whichOverlays.includes(c.DEPTH_MAP_OVERLAY);
  return (
    <div className={`buttons ${st.videoSelector}`}>
      <Button
        isSelected={isSelected}
        onClick={() => onSelect(c.DEPTH_MAP_OVERLAY)}
      >
        Depth Map
      </Button>
    </div>
  );
}

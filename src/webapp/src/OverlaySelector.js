import React from "react";

import * as c from "./constants";
import { Button } from "./components/Button";

import st from "./OverlaySelector.module.css";

export function OverlaySelector({ whichOverlays, onSelect }) {
  return (
    <div className={st.overlaySelector}>
      <Button
        isSelected={whichOverlays.includes(c.DEPTH_MAP_OVERLAY)}
        onClick={() => onSelect(c.DEPTH_MAP_OVERLAY)}
      >
        Depth Map
      </Button>
      <Button
        isSelected={whichOverlays.includes(c.OBJECTS_OVERLAY)}
        onClick={() => onSelect(c.OBJECTS_OVERLAY)}
      >
        Objects
      </Button>
    </div>
  );
}

import React from "react";

import * as c from "./constants";
import { DepthMapOverlay } from "./DepthMapOverlay";
import { ObjectsOverlay } from "./ObjectsOverlay";
import st from "./Overlays.module.css";

export function Overlays({
  whichOverlays,
  filterConfidence,
  hubState,
  children,
}) {
  return (
    <div className={st.overlayContainer}>
      <div className={st.overlay}>
        {whichOverlays.includes(c.DEPTH_MAP_OVERLAY) && (
          <DepthMapOverlay depthMap={hubState.depth_map.section_map} />
        )}
        {whichOverlays.includes(c.OBJECTS_OVERLAY) && (
          <ObjectsOverlay
            objects={hubState.recognition}
            filterConfidence={filterConfidence}
          />
        )}
      </div>
      {children}
    </div>
  );
}

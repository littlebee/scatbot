import React from "react";

import * as c from "./constants";
import { DepthMapOverlay } from "./DepthMapOverlay";
import st from "./Overlays.module.css";

export function Overlays({ whichOverlays, depthMap, children }) {
  return (
    <div className={st.overlayContainer}>
      <div className={st.overlay}>
        {whichOverlays.includes(c.DEPTH_MAP_OVERLAY) && (
          <DepthMapOverlay depthMap={depthMap} />
        )}
      </div>
      {children}
    </div>
  );
}

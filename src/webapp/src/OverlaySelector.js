import React from "react";

import * as c from "./constants";
import { Button } from "./components/Button";
import { ButtonFaderCombo } from "./components/ButtonFaderCombo";

import st from "./OverlaySelector.module.css";

export function OverlaySelector({
  whichOverlays,
  onSelect,
  filterConfidence,
  onFilterConfidence,
}) {
  const handleFade = (pct) => {
    // we flip the percentage such that
    // more fader = more objects = lower confidence
    onFilterConfidence(1 - pct);
  };

  const fadeMessage = `min confidence: ${filterConfidence.toFixed(2)}`;

  return (
    <div className={st.overlaySelector}>
      <Button
        isSelected={whichOverlays.includes(c.DEPTH_MAP_OVERLAY)}
        onClick={() => onSelect(c.DEPTH_MAP_OVERLAY)}
      >
        Depth Map
      </Button>
      <ButtonFaderCombo
        isSelected={whichOverlays.includes(c.OBJECTS_OVERLAY)}
        fadePercent={1 - filterConfidence}
        onClick={() => onSelect(c.OBJECTS_OVERLAY)}
        onFade={handleFade}
        fadeMessage={fadeMessage}
      >
        Objects
      </ButtonFaderCombo>
    </div>
  );
}

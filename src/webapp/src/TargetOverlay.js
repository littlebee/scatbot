import React from "react";

import st from "./TargetOverlay.module.css";

export function TargetOverlay({ behavior }) {
  if (!behavior.targetAcquired || behavior.targetBoundingBox.length <= 0) {
    return null;
  }
  const [left, top, right, bottom] = behavior.targetBoundingBox;

  const style = {
    top,
    left,
    height: bottom - top,
    width: right - left,
  };
  return (
    <div className={st.wrapper}>
      <div className={st.objectSquare} style={style} />
    </div>
  );
}

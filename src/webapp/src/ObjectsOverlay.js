import React from "react";

import st from "./ObjectsOverlay.module.css";

export function ObjectsOverlay({ objects }) {
  if (!objects || objects.length < 1) {
    return null;
  }
  const elements = [];
  for (let obj of objects) {
    const [left, top, right, bottom] = obj.boundingBox;

    const style = {
      top,
      left,
      height: bottom - top,
      width: right - left,
    };
    elements.push(
      <div className={st.objectSquare} style={style}>
        <div className={st.objectClassification}>{obj.classification}</div>
        <div className={st.objectConfidence}>{obj.confidence.toFixed(3)}</div>
      </div>
    );
  }
  return <>{elements}</>;
}
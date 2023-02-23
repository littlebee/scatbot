import React from "react";

import st from "./ObjectsOverlay.module.css";

export function ObjectsOverlay({ objects, filterConfidence }) {
  if (!objects || objects.length < 1) {
    return null;
  }
  const elements = [];
  for (let obj of objects) {
    if (obj.confidence < filterConfidence) {
      continue;
    }
    const [left, top, right, bottom] = obj.boundingBox;

    const style = {
      top,
      left,
      height: bottom - top,
      width: right - left,
    };
    elements.push(
      <div className={st.objectSquare} style={style} key={left * top}>
        <div className={st.objectClassification}>{obj.classification}</div>
        <div className={st.objectConfidence}>{obj.confidence.toFixed(3)}</div>
      </div>
    );
  }
  return <div className={st.wrapper}>{elements}</div>;
}

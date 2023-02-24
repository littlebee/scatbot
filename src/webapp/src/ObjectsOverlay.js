import React from "react";
import { v4 as uuidv4 } from "uuid";

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
    // Use a uuid key here because we don't have a good way of uniquely identifying
    // these and having diff objects with the same key causes React to leave ghost
    // recog objects that wont go away until you turn off the overlay
    elements.push(
      <div className={st.objectSquare} style={style} key={uuidv4()}>
        <div className={st.objectClassification}>{obj.classification}</div>
        <div className={st.objectConfidence}>{obj.confidence.toFixed(3)}</div>
      </div>
    );
  }
  return <div className={st.wrapper}>{elements}</div>;
}

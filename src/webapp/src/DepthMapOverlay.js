import React from "react";

import st from "./DepthMapOverlay.module.css";

export function DepthMapOverlay({ depthMap }) {
  if (!depthMap) {
    return null;
  }
  const elements = [];
  depthMap.forEach((row) => {
    row.forEach((col) => {
      elements.push(<div className={st.depthSquare}>{col}cm</div>);
    });
  });
  return <>{elements}</>;
}

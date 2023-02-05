import React from "react";

import st from "./DepthMapOverlay.module.css";

export function DepthMapOverlay({ depthMap }) {
  if (!depthMap) {
    return null;
  }
  const elements = [];
  const width = 640 / depthMap[0].length;
  const height = 480 / depthMap.length;
  depthMap.forEach((row, yi) => {
    row.forEach((col, xi) => {
      const style = {
        width,
        height,
        top: yi * height,
        left: xi * width,
      };

      elements.push(
        <div className={st.depthSquare} style={style}>
          <div className={st.depthValue}>{col / 10}</div>
        </div>
      );
    });
  });
  return <>{elements}</>;
}

import React, { useEffect, useState, useRef, useMemo } from "react";
import { sendThrottles } from "./hub-state";

// import { sendThrottles } from "./hub-state.js";

import st from "./Hazards.module.css";

const INDICATORS = [
  {
    name: "front right hazard",
    hazards_key: "front",
    sensor: 0,
    right: 45,
    bottom: 285,
  },
  {
    name: "front left hazard",
    hazards_key: "front",
    sensor: 1,
    right: 175,
    bottom: 285,
  },
  {
    name: "front center hazard",
    hazards_key: "front",
    sensor: 2,
    right: 110,
    bottom: 310,
  },
  {
    name: "front bottom hazard",
    hazards_key: "front",
    sensor: 3,
    right: 110,
    bottom: 285,
  },
];

const HAZARD_TYPE_COLORS = {
  cliff: "#FF0000",
  collision: "#FFC000",
};

export function Hazards({ hubState }) {
  const frontHazardsBySensor = useMemo(
    () =>
      Object.fromEntries(
        hubState.hazards.front.map((hazard) => [hazard.sensor, hazard.type])
      ),
    [hubState.hazards]
  );

  return (
    <div className={st.hazardsContainer}>
      <img src="/scatbot-overlay.png" />
      {INDICATORS.map((indicator) => {
        const hazardType = frontHazardsBySensor[indicator.sensor];
        const style = {
          right: indicator.right,
          bottom: indicator.bottom,
        };
        if (hazardType) {
          style.backgroundColor = HAZARD_TYPE_COLORS[hazardType];
        }
        return (
          <div key={indicator.sensor} className={st.indicator} style={style} />
        );
      })}
    </div>
  );
}

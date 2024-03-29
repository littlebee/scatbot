import React, { useEffect, useState, useRef, useMemo } from "react";
import { sendThrottles } from "./hub-state";

// import { sendThrottles } from "./hub-state.js";

import st from "./Hazards.module.css";
import { classnames } from "./util/classNames";

const INDICATORS = [
  {
    name: "front left hazard",
    hazards_key: "front",
    sensor: 0,
    left: "22%",
    top: -5,
  },
  {
    name: "front right hazard",
    hazards_key: "front",
    sensor: 1,
    left: "63%",
    top: -5,
  },
  {
    name: "front center hazard",
    hazards_key: "front",
    sensor: 2,
    left: "42%",
    top: -25,
  },
  {
    name: "rear left hazard",
    hazards_key: "rear",
    sensor: 3,
    left: "22%",
    top: 270,
  },
  {
    name: "rear right hazard",
    hazards_key: "rear",
    sensor: 4,
    left: "63%",
    top: 270,
  },
  {
    name: "rear center hazard",
    hazards_key: "rear",
    sensor: 5,
    left: "42%",
    top: 285,
  },
];

const HAZARD_TYPE_COLORS = {
  cliff: "#FF0000",
  collision: "#FF5000",
};

export function Hazards({ hubState }) {
  const hazardsBySensor = useMemo(() => {
    const frontHazards = Object.fromEntries(
      hubState.hazards.front.map((hazard) => [hazard.sensor, hazard.type])
    );
    const rearHazards = Object.fromEntries(
      hubState.hazards.rear.map((hazard) => [hazard.sensor, hazard.type])
    );
    return { ...frontHazards, ...rearHazards };
  }, [hubState.hazards]);

  const isRemoteControl = hubState.behavior.mode === 0;

  const containerClass = classnames(st.hazardsContainer, {
    predicate: !isRemoteControl,
    value: st.smallerContainer,
  });

  const indicatorClass = classnames(st.indicator, {
    predicate: !isRemoteControl,
    value: st.smallerIndicator,
  });

  return (
    <div className={containerClass}>
      <img className={st.image} src="/scatbot-overlay.png" />
      {INDICATORS.map((indicator) => {
        const hazardType = hazardsBySensor[indicator.sensor];
        const style = {
          top: indicator.top,
          left: indicator.left,
        };
        if (hazardType) {
          style.backgroundColor = HAZARD_TYPE_COLORS[hazardType];
        }
        return (
          <div
            key={indicator.sensor}
            className={indicatorClass}
            style={style}
            title={`${indicator.name} - ${hazardType}`}
          />
        );
      })}
    </div>
  );
}

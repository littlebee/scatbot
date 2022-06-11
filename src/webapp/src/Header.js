import React, { useState } from "react";

import { LabeledText } from "./components/LabeledText";

import { classnames } from "./util/classNames";
import st from "./Header.module.css";

export function Header({
  hubState,
  isHubStateDialogOpen,
  onHubStateDialogOpen,
}) {
  const system_stats = hubState.system_stats;

  const dialogCls = classnames("wrap", st.header);
  const topLeftCls = classnames(
    "left-frame-top",
    "sidebar-buttons",
    st.leftFrameTop,
    {
      predicate: isHubStateDialogOpen,
      value: st.activeDialogTrigger,
    }
  );

  return (
    <div className={dialogCls}>
      <div className={topLeftCls} onClick={onHubStateDialogOpen}>
        Hub State
      </div>

      <div className="right-frame-top">
        <div className={`padded-1 flex-row`}>
          <div className={st.rightFrameContent}>
            <div className={`flex-row ${st.stats}`}>
              <div className={st.statsColumn}>
                <LabeledText label="hub status">
                  {hubState.hubConnStatus}
                </LabeledText>
                {hubState.hubConnStatus === "online" && (
                  <LabeledText label="battery">
                    {hubState.battery?.voltage.toFixed(1)}V@
                    {hubState.battery?.current.toFixed(1)}A
                  </LabeledText>
                )}
              </div>
              {hubState.hubConnStatus === "online" && (
                <>
                  <div className={st.statsColumn}>
                    <LabeledText label="cpu temp">
                      {system_stats?.cpu_temp.toFixed(1)}˚
                    </LabeledText>
                    <LabeledText label="cpu util">
                      {system_stats?.cpu_util.toFixed(1)}%
                    </LabeledText>
                    <LabeledText label="ram util">
                      {system_stats?.ram_util.toFixed(1)}%
                    </LabeledText>
                  </div>

                  <div className={st.statsColumn}>
                    <LabeledText label="compass">
                      {hubState.compass?.toFixed(1)}˚
                    </LabeledText>
                    <LabeledText label="min dist">
                      {hubState.depth_map?.min_distance?.toFixed(1)}cm
                    </LabeledText>
                    <LabeledText label="max dist">
                      {hubState.depth_map?.max_distance?.toFixed(1)}cm
                    </LabeledText>
                  </div>
                </>
              )}
            </div>
          </div>
          <div className={st.title}>
            <h1>scatbot</h1>
          </div>
        </div>
        <div className="top-corner-bg">
          <div className="top-corner"></div>
        </div>
        <div className="bar-panel">
          <div className="bar-1"></div>
          <div className="bar-2"></div>
          <div className="bar-3"></div>
          <div className="bar-4">
            <div className="bar-4-inside"></div>
          </div>
          <div className="bar-5"></div>
        </div>
      </div>
    </div>
  );
}

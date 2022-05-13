import React, { useState } from "react";

import { classnames } from "./util/classNames";
import st from "./Header.module.css";

export function Header({
  hubState,
  isHubStateDialogOpen,
  onHubStateDialogOpen,
}) {
  const system_stats = hubState.system_stats.get();

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
          <div className={`flex-column flex-grow`}>
            <div className={`flex-row ${st.stats}`}>
              <div className={st.statsColumn}>
                <div className={st.statsRow}>
                  <div className={st.statsLabel}>hub status:</div>
                  <div>{hubState.hubConnStatus.get()}</div>
                </div>

                <div className={st.statsRow}>
                  <div className={st.statsLabel}>cpu temp:</div>
                  <div>{system_stats?.cpu_temp.toFixed(1)}˚</div>
                </div>

                <div className={st.statsRow}>
                  <div className={st.statsLabel}>cpu util:</div>
                  <div>{system_stats?.cpu_util.toFixed(1)}%</div>
                </div>

                <div className={st.statsRow}>
                  <div className={st.statsLabel}>ram util:</div>
                  <div>{system_stats?.ram_util.toFixed(1)}%</div>
                </div>
              </div>

              <div className={st.statsColumn}>
                <div className={st.statsRow}>
                  <div className={st.statsLabel}>compass:</div>
                  <div>{hubState.compass.get().toFixed(1)}˚</div>
                </div>
              </div>
            </div>
          </div>
          <div>
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

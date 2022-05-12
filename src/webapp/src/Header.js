import React from "react";
import st from "./Header.module.css";

export function Header({ hubState }) {
  const system_stats = hubState.system_stats.get();

  return (
    <div className={`wrap ${st.header}`}>
      <div className="left-frame-top"></div>

      <div className="right-frame-top">
        <div className={`padded-1 flex-row`}>
          <div className={`flex-column flex-grow`}>
            <div className={`flex-row ${st.stats}`}>
              <div className={st.statsColumn}>
                <div>
                  <label>hub status:</label>
                  <span>{hubState.hubConnStatus.get()}</span>
                </div>
                <div>
                  <label>cpu temp:</label>
                  <span>{system_stats?.cpu_temp.toFixed(1)}˚</span>
                </div>

                <div>
                  <label>cpu util:</label>
                  <span>{system_stats?.cpu_util.toFixed(1)}%</span>
                </div>
                <div>
                  <label>ram util:</label>
                  <span>{system_stats?.ram_util.toFixed(1)}%</span>
                </div>
              </div>
              <div className={st.statsColumn}>
                <div>
                  <label>compass:</label>
                  <span>{hubState.compass.get().toFixed(1)}˚</span>
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

import React from "react";
import st from "./Header.module.css";

export function Header({ hubState }) {
  return (
    <div className={`wrap ${st.header}`}>
      <div className="left-frame-top"></div>

      <div className="right-frame-top">
        <div className="padded-1 flex-row">
          <div className="flex-column flex-grow">
            <div>
              <label>hub status:</label>
              <span>{hubState.hubConnStatus.get()}</span>
            </div>

            <div> compass: {hubState.compass.get()}</div>
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

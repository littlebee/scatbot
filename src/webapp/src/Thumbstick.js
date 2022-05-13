import React, { useEffect, useState, useRef } from "react";
import { sendThrottles } from "./hub-state";

// import { sendThrottles } from "./hub-state.js";

import st from "./Thumbstick.module.css";

export function Thumbstick() {
  // hang these off of document so we get them when you
  // release outside the container
  useEffect(() => {
    document.addEventListener("mouseup", handleMouseUp);
    document.addEventListener("touchend", handleMouseUp);
    document.addEventListener("touchcancel", handleMouseUp);
    return () => {
      document.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("touchend", handleMouseUp);
      document.removeEventListener("touchcancel", handleMouseUp);
    };
  }, []);

  const [relativeX, setRelativeX] = useState(0);
  const [relativeY, setRelativeY] = useState(0);
  const [mouseIsDown, setMouseIsDown] = useState(false);
  const containerRef = useRef();

  function getClientXY(event) {
    return [
      event.clientX || event.touches[0].clientX,
      event.clientY || event.touches[0].clientY,
    ];
  }

  const handleMouseDown = (event) => {
    setMouseIsDown(true);

    setRelativePosition(...getClientXY(event));
  };

  const handleMouseMove = (event) => {
    if (mouseIsDown) {
      setRelativePosition(...getClientXY(event));
    }
  };

  const handleMouseUp = () => {
    setMouseIsDown(false);
    sendThrottles(0, 0);
    setRelativeX(0);
    setRelativeY(0);
  };

  const setRelativePosition = (clientX, clientY) => {
    const relativeX = clientX - containerRef.current.offsetLeft - 100;
    const relativeY = -1 * (clientY - containerRef.current.offsetTop - 100);
    console.log("computed offsets", { relativeX, relativeY });
    setRelativeX(relativeX);
    setRelativeY(relativeY);

    let leftThrottle = 0;
    let rightThrottle = 0;
    // if the stick is mostly centered vertically, then we are going
    // to turn like a tank and spin the motors in opposite directions
    if (Math.abs(relativeY <= 15)) {
      console.log("doing tank turn");
      leftThrottle = relativeX / 100;
      rightThrottle = leftThrottle * -1;
    } else {
      const maxThrottle = relativeY / 100;
      // if you are, for example at the top of the Y, and a little to the right,
      // the right motor needs to be lower than the left by an amount relative
      // to the x coord of the stick
      leftThrottle =
        relativeX < 15
          ? maxThrottle + maxThrottle * (relativeX / 100)
          : maxThrottle;
      rightThrottle =
        relativeX > 15
          ? maxThrottle - maxThrottle * (relativeX / 100)
          : maxThrottle;
    }

    sendThrottles(leftThrottle, rightThrottle);
  };

  const top = 95 + relativeY * -1;
  const left = 95 + relativeX;

  return (
    <div
      className={st.thumbstickContainer}
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onTouchStart={handleMouseDown}
      onMouseMove={handleMouseMove}
      onTouchMove={handleMouseMove}
    >
      <div className={st.thumbstickPosition} style={{ top, left }} />
    </div>
  );
}

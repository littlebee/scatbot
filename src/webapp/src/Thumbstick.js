import React, { useEffect, useState, useRef } from "react";
import { sendThrottles } from "./hub-state";

// import { sendThrottles } from "./hub-state.js";

import st from "./Thumbstick.module.css";

// container element is 2x this width and height
const STICK_RADIUS = 100;

export function Thumbstick() {
  // hang these off of document so we get them when you
  // release outside the container element
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

  // stick throttles are now at 0 - 1 scale.  Motors will not turn
  // at less than 0.5 so set that as the min and scale the remain
  // by the stick throttles
  const governThrottle = (stickThrottle) => {
    const minThrottle = stickThrottle > 0 ? 0.5 : -0.5;
    const throttleRange = 1 - Math.abs(minThrottle);

    return minThrottle + stickThrottle * throttleRange;
  };

  const setRelativePosition = (clientX, clientY) => {
    const relativeX = clientX - containerRef.current.offsetLeft - STICK_RADIUS;
    const relativeY =
      -1 * (clientY - containerRef.current.offsetTop - STICK_RADIUS);

    console.log("computed offsets", { relativeX, relativeY });

    setRelativeX(relativeX);
    setRelativeY(relativeY);

    let leftThrottle = 0;
    let rightThrottle = 0;
    // if the stick is mostly centered vertically, then we are going
    // to turn like a tank and spin the motors in opposite directions
    if (Math.abs(relativeY) <= 15) {
      console.log("doing tank turn");
      leftThrottle = governThrottle(relativeX / STICK_RADIUS);
      rightThrottle = governThrottle(leftThrottle * -1);
    } else {
      const maxThrottle = relativeY / STICK_RADIUS;
      // if you are, for example, at the top of the Y and a little to the right,
      // the right motor needs to be lower than the left by an amount relative
      // to the x coord of the stick
      leftThrottle = governThrottle(
        relativeX < 15
          ? maxThrottle + maxThrottle * (relativeX / STICK_RADIUS)
          : maxThrottle
      );
      rightThrottle = governThrottle(
        relativeX > 15
          ? maxThrottle - maxThrottle * (relativeX / STICK_RADIUS)
          : maxThrottle
      );
    }
    console.log("sending throttles", { leftThrottle, rightThrottle });
    sendThrottles(leftThrottle, rightThrottle);
  };

  const top = 95 + relativeY * -1;
  const left = 95 + relativeX;

  const containerStyle = {
    width: STICK_RADIUS * 2,
    height: STICK_RADIUS * 2,
  };

  const stickStyle = { top, left };

  return (
    <div
      className={st.thumbstickContainer}
      style={containerStyle}
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onTouchStart={handleMouseDown}
      onMouseMove={handleMouseMove}
      onTouchMove={handleMouseMove}
    >
      <div className={st.thumbstickPosition} style={stickStyle} />
    </div>
  );
}

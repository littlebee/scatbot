import { useState, useEffect } from "react";
import * as c from "./constants";

const VIDEO_HOST =
  !process.env.NODE_ENV || process.env.NODE_ENV === "development"
    ? "scatbot.local:5001"
    : `${window.location.hostname}:5001`;

export function VideoFeed({ whichVideo }) {
  const [rand, setRand] = useState(0);
  const [errorMsg, setErrorMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setInterval(() => {
      setIsLoading(true);
      setRand(Math.random());
    }, 30000);
  }, []);

  useEffect(() => {
    setErrorMessage(null);
  }, [whichVideo]);

  const handleError = (e) => {
    console.log("got error from image load", e);
    setErrorMessage(`Unable to get video feed from ${VIDEO_HOST}`);
  };

  const handleLoad = (e) => {
    console.log("video feed loaded");
    setErrorMessage(null);
    setIsLoading(false);
  };

  const feed_path = whichVideo === c.DEPTH_VIDEO ? "depth_feed" : "video_feed";
  const feedUrl = `http://${VIDEO_HOST}/${feed_path}?rand=${rand}`;
  const imgClass = `pics video-feed ${isLoading || errorMsg ? "loading" : ""}`;
  return (
    <>
      {(isLoading || errorMsg) && (
        <img
          className="standby-image"
          alt="please stand by"
          src="/please-stand-by.png"
        />
      )}
      <img
        className={imgClass}
        alt="video feed"
        src={feedUrl}
        onError={handleError}
        onLoad={handleLoad}
      />
    </>
  );
}

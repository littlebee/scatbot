import { useState, useEffect } from "react";

const VIDEO_HOST =
  !process.env.NODE_ENV || process.env.NODE_ENV === "development"
    ? "scatbot.local:5001"
    : `${window.location.hostname}:5001`;

export function VideoFeed() {
  const [rand, setRand] = useState(0);
  const [errorMsg, setErrorMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setInterval(() => {
      setIsLoading(true);
      setRand(Math.random());
      // setErrorMessage(null);
    }, 600000);
  }, []);

  const handleError = (e) => {
    console.log("got error from image load", e);
    setErrorMessage(`Unable to get video feed from ${VIDEO_HOST}`);
  };

  const handleLoad = (e) => {
    console.log("video feed loaded");
    setIsLoading(false);
  };

  const feedUrl = `http://${VIDEO_HOST}/video_feed?rand=${rand}`;
  return (
    <div>
      {(isLoading || errorMsg) && (
        <img
          className="standby-image"
          alt="please stand by"
          src="/please-stand-by.png"
        />
      )}
      <img
        className="pics"
        alt="video feed"
        src={feedUrl}
        onError={handleError}
        onLoad={handleLoad}
      />
    </div>
  );
}

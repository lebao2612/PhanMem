import { useRef, useState } from "react";

function RightSideLogin() {
  const videoRef = useRef(null);
  const [showPlay, setShowPlay] = useState(true);

  const handleVideoClick = () => {
    const video = videoRef.current;
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  };
  return (
    <>
      <div className="w-6/10 flex flex-col justify-center items-center text-center px-12 bg-[#111]">
        <h2 className="text-4xl font-bold mb-4">
          Ý tưởng cho{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-cyan-400">
            Video
          </span>{" "}
        </h2>
        <p className="text-sm text-gray-400 mb-6 max-w-md">
          Với invideo AI, bạn có thể tạo video quảng cáo cho mạng xã hội chỉ
          trong vài phút.{" "}
        </p>

        <div className="relative">
          <video
            ref={videoRef}
            src="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/Gen3Promo.mp4"
            poster="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/poster-images/Gen3Promo.jpeg"
            className="rounded-lg w-[700px] h-auto shadow-lg cursor-pointer"
            playsInline
            onClick={handleVideoClick}
            onPlay={() => setShowPlay(false)}
            onPause={() => setShowPlay(true)}
          />
          {showPlay && (
            <button
              className="absolute inset-0 flex items-center justify-center pointer-events-none"
              style={{ zIndex: 2 }}
              tabIndex={-1}
              aria-label="Play"
            >
              <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                <circle cx="40" cy="40" r="40" fill="#fff" fillOpacity="0.3" />
                <polygon
                  points="32,25 60,40 32,55"
                  fill="#fff"
                  fillOpacity="0.8"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </>
  );
}

export default RightSideLogin;

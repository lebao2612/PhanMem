"use client";

import { useRef, useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import GoogleLoginButton from "../components/GoogleLoginButton";

function Login() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const hasNavigated = useRef(false);
  const videoRef = useRef(null);
  const [showPlay, setShowPlay] = useState(true);

  useEffect(() => {
    const storedUser = sessionStorage.getItem("user");
    if (storedUser && !user) {
      setUser(JSON.parse(storedUser));
    }
  }, [setUser, user]);

  useEffect(() => {
    if (user && !hasNavigated.current) {
      hasNavigated.current = true;
      navigate("/home");
    }
  }, [user, navigate]);

  const handleVideoClick = () => {
    const video = videoRef.current;
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-zinc-900 to-black text-white flex items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-[#111] rounded-2xl shadow-2xl p-4 flex flex-col items-center text-center space-y-6">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <img
            src="https://assets.wheelhouse.com/media/_solution_logo_04102024_26667162.png"
            alt="invideo AI logo"
            className="w-8 h-8 rounded-full"
          />
          <span className="text-xl font-semibold">invideo AI</span>
        </div>

        {/* Tiêu đề chính */}
        <h1 className="text-3xl md:text-4xl font-bold">
          Chào mừng đến với{" "}
          <span className="bg-gradient-to-r from-blue-400 to-cyan-400 text-transparent bg-clip-text">
            invideo AI
          </span>
        </h1>

        {/* Nút đăng nhập */}
        <GoogleLoginButton />

        {/* Video demo */}
        <div className="relative w-full mt-6">
          <video
            ref={videoRef}
            src="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/Gen3Promo.mp4"
            poster="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/poster-images/Gen3Promo.jpeg"
            className="rounded-lg w-full h-auto shadow-lg cursor-pointer"
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

        {/* Mô tả */}
        <p className="text-sm text-gray-400">
          Tạo video quảng cáo chuyên nghiệp cho mạng xã hội chỉ trong vài phút với AI.
        </p>
      </div>
    </div>
  );
}

export default Login;

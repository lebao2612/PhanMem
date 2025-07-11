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
  const [showStartButton, setShowStartButton] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [videoBlurred, setVideoBlurred] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);
  const hasHandledCodeRef = useRef(false);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const error = urlParams.get("error");
    const state = urlParams.get("state");

    if (error === "access_denied") {
      alert("Bạn đã từ chối đăng nhập bằng Google");
      return;
    }

    if (sessionStorage.getItem("token") || user) {
      return;
    }

    if (code && !hasHandledCodeRef.current) {
      hasHandledCodeRef.current = true;
      const doGoogleLogin = async () => {
        try {
          // const res = await fetch(`/api/auth/google/callback?code=${code}`);
          const res = await fetch(`/api/auth/google/callback?code=${code}${state ? `&state=${state}` : ""}`);
          const { success, data, error } = await res.json();

          if (!res.ok || !success)
            throw new Error(error?.message || "Lỗi xác thực Google");

          const userInfo = {
            name: data.user.name || data.user.email,
            email: data.user.email,
          };

          setUser(userInfo);
          sessionStorage.setItem("token", data.token);
          sessionStorage.setItem("user", JSON.stringify(userInfo));
          navigate("/home");
        } catch (err) {
          alert("Đăng nhập Google thất bại");
          console.error(err);
          navigate("/login");
        }
      };
      doGoogleLogin();
    }
  }, []);

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

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      // Auto play video
      video
        .play()
        .then(() => {
          console.log("Video started playing");
          // Sau 3 giây thì bắt đầu blur và tối màu
          setTimeout(() => {
            setVideoBlurred(true);
            setShowOverlay(true);
            // Hiển thị nút start sau khi blur
            setTimeout(() => {
              setShowStartButton(true);
            }, 500); // Delay thêm 0.5s để hiệu ứng mượt hơn
          }, 3000);
        })
        .catch((error) => {
          console.log("Auto-play failed:", error);
        });
    }
  }, []);

  const handleStartClick = () => {
    setShowPopup(true);
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Video full screen */}
      <video
        ref={videoRef}
        src="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/Gen3Promo.mp4"
        poster="https://web-assets.invideo.io/landing-pages/prod/homepage/videos/poster-images/Gen3Promo.jpeg"
        className="absolute inset-0 w-full h-full object-cover transition-all duration-1000"
        style={{
          filter: videoBlurred ? "blur(3px)" : "blur(0px)",
        }}
        playsInline
        muted
        loop
      />

      {/* Overlay tối xuất hiện sau 3s */}
      <div
        className={`absolute inset-0 bg-black transition-opacity duration-1000 ${
          showOverlay ? "opacity-50" : "opacity-0"
        }`}
      />

      {/* Overlay thêm khi popup mở để video tối hơn */}
      {showPopup && (
        <div className="absolute inset-0 bg-black opacity-30 z-40" />
      )}

      {/* Nút Start Generate Video - chỉ ẩn khi popup mở */}
      {showStartButton && !showPopup && (
        <div className="absolute inset-0 flex items-center justify-center z-10 animate-fade-in-up">
          <div className="text-center space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 animate-slide-down">
              Create professional AI videos
            </h1>
            <p className="text-xl text-gray-200 mb-8 animate-slide-down-delay">
              In just minutes with advanced AI technology
            </p>
            <button
              onClick={handleStartClick}
              className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-bold py-4 px-8 rounded-full text-xl shadow-2xl transform hover:scale-105 transition-all duration-300 animate-bounce-in"
            >
              Start generate video →
            </button>
          </div>
        </div>
      )}

      {/* Popup Modal - hiển thị trên video */}
      {showPopup && (
        <div className="absolute inset-0 flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="bg-[#111] bg-opacity-95 backdrop-blur-sm rounded-2xl shadow-2xl p-8 max-w-md w-full text-center space-y-6 relative border border-gray-800 animate-scale-in">
            {/* Nút đóng */}
            <button
              onClick={closePopup}
              className="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl hover:rotate-90 transition-transform duration-200"
            >
              ×
            </button>

            {/* Logo và tiêu đề */}
            <div className="flex items-center justify-center space-x-3 animate-slide-down">
              <img
                src="https://assets.wheelhouse.com/media/_solution_logo_04102024_26667162.png"
                alt="invideo AI logo"
                className="w-10 h-10 rounded-full"
              />
              <span className="text-2xl font-bold text-white">Invideo AI</span>
            </div>

            {/* Mô tả */}
            <p className="text-gray-300 text-lg animate-slide-up">
              Create professional AI videos in just minutes
            </p>

            {/* Nút đăng nhập Google */}
            <div className="pt-4 animate-slide-up-delay">
              <GoogleLoginButton />
            </div>
          </div>
        </div>
      )}
      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slide-down {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes scale-in {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        @keyframes bounce-in {
          0% {
            opacity: 0;
            transform: scale(0.3);
          }
          50% {
            transform: scale(1.05);
          }
          70% {
            transform: scale(0.9);
          }
          100% {
            opacity: 1;
            transform: scale(1);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }

        .animate-fade-in-up {
          animation: fade-in-up 0.8s ease-out;
        }

        .animate-slide-down {
          animation: slide-down 0.6s ease-out;
        }

        .animate-slide-down-delay {
          animation: slide-down 0.6s ease-out 0.2s both;
        }

        .animate-slide-up {
          animation: slide-up 0.5s ease-out 0.1s both;
        }

        .animate-slide-up-delay {
          animation: slide-up 0.5s ease-out 0.3s both;
        }

        .animate-scale-in {
          animation: scale-in 0.4s ease-out;
        }

        .animate-bounce-in {
          animation: bounce-in 0.8s ease-out 0.4s both;
        }
      `}</style>
    </div>
  );
}

export default Login;

"use client";

import { useEffect, useContext, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import images from "../assets/images";

const LoginGoogleCallbackPage = () => {
  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);
  const hasHandledCodeRef = useRef(false);
  const [isLoading, setIsLoading] = useState(true); // Trạng thái hiển thị popup

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const state = urlParams.get("state");
    const error = urlParams.get("error");

    if (error === "access_denied") {
      alert("Bạn đã từ chối đăng nhập bằng Google");
      navigate("/login");
      return;
    }

    if (!code || hasHandledCodeRef.current) {
      return;
    }

    hasHandledCodeRef.current = true;

    const fetchUser = async () => {
      try {
        const res = await fetch(
          `/api/auth/google/callback?code=${code}${state ? `&state=${state}` : ""}`
        );
        const { success, data, error } = await res.json();

        if (!res.ok || !success) {
          throw new Error(error?.message || "Lỗi xác thực Google");
        }

        setUser(data.user);
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("user", JSON.stringify(data.user));

        // Làm sạch URL
        window.history.replaceState({}, document.title, "/");

        // Đợi ít nhất 2 giây trước khi điều hướng
        setTimeout(() => {
          setIsLoading(false);
          navigate("/home");
        }, 10000);
      } catch (err) {
        console.error("Google login failed:", err);
        alert(err.message || "Đăng nhập Google thất bại");
        setIsLoading(false);
        navigate("/login");
      }
    };

    fetchUser();
  }, [navigate, setUser]);

  return (
    <div
      className="min-h-screen flex items-center justify-center text-white"
      style={{
        backgroundImage: `url(${images.callbackBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        filter: "grayscale(50%)",
      }}
    >
      {isLoading && (
        <div
          className="absolute top-[30%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black bg-opacity-80 p-10 rounded-xl text-center w-[350px] h-[180px] scale-[1.2] font-sans animate-fadeIn"
        >
          {/* Logo + Text */}
          <div className="flex items-center justify-center space-x-3">
            <img
              src={
                images.invideoAILogo ||
                "https://assets.wheelhouse.com/media/_solution_logo_04102024_26667162.png"
              }
              alt="invideo AI logo"
              className="w-10 h-10 rounded-full"
            />
            <span className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-blue-900 bg-clip-text text-transparent">
              Invideo AI
            </span>
          </div>
  
          {/* Đường kẻ xám */}
          <div className="border-b border-gray-500 my-6" />
  
          {/* Dòng thông báo */}
          <div className="text-sm text-white mt-4">Đang đăng nhập với Google...</div>
        </div>
      )}
  
      {/* Animation style */}
      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-in-out;
        }
      `}</style>
    </div>
  );
};

export default LoginGoogleCallbackPage;
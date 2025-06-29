import { useEffect, useContext, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

const googleOAuthCallback = () => {
  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);
  const hasHandled = useRef(false);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get("error");
    const code = urlParams.get("code");

    // Trường hợp người dùng từ chối cấp quyền
    if (error === "access_denied") {
      navigate("/login");
      return;
    }

    if (!code || hasHandled.current) return;

    hasHandled.current = true;

    const doGoogleLogin = async () => {
      try {
        const res = await fetch(`/api/auth/google/callback?code=${code}`);
        const { success, data, error } = await res.json();
        if (!res.ok || !success) throw new Error(error?.message || "Lỗi xác thực từ Google");

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
  }, [navigate, setUser]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-zinc-900 to-black text-white flex items-center justify-center">
      <p className="text-lg font-semibold mb-4">Đang đăng nhập bằng Google...</p>
    </div>
  );
};

export default googleOAuthCallback;

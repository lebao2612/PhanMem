"use client";

import { useRef, useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import RightSideLogin from "../components/RightSideLogin";
import GoogleLoginButton from "../components/GoogleLoginButton";

function Login() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const hasNavigated = useRef(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

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

  const handleGoogleLoginSuccess = (data) => {
    const user = data.user;
    const token = data.token;

    const userInfo = {
      name: user.name || user.email,
      email: user.email,
    };

    setUser(userInfo);
    sessionStorage.setItem("token", token);
    sessionStorage.setItem("user", JSON.stringify(userInfo));
  };

  const handleGoogleLoginError = (error) => {
    alert("Login failed. Please try again.");
    console.error("Login failed:", error);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Đăng nhập thất bại");
      }

      const userInfo = {
        name: data.user.name || data.user.email,
        email: data.user.email,
      };

      setUser(userInfo);
      sessionStorage.setItem("user", JSON.stringify(userInfo));
      sessionStorage.setItem("token", data.token);
    } catch (error) {
      setError(error.message);
      console.error("Lỗi đăng nhập:", error.message);
    }
  };

  return (
    <div className="flex min-h-screen text-white bg-black">
      <div className="w-4/10 flex flex-col justify-center px-12">
        <div className="flex items-center mb-8">
          <img
            className="w-6 h-6 rounded-full mr-2"
            src="https://assets.wheelhouse.com/media/_solution_logo_04102024_26667162.png"
            alt="invideo AI logo"
          />
          <p className="text-lg font-semibold">invideo AI</p>
        </div>

        <h1 className="text-4xl font-bold mb-6">
          Chào mừng đến với{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
            invideo AI
          </span>
        </h1>

        <div className="w-full flex flex-col items-center">
          <GoogleLoginButton
            onSuccess={handleGoogleLoginSuccess}
            onError={handleGoogleLoginError}
          />
        </div>

        <div className="text-center text-sm text-gray-500 my-2">Hoặc</div>

        <form onSubmit={handleLogin} className="w-full flex flex-col items-center">
          <input type="text" style={{ display: "none" }} />
          <input type="password" style={{ display: "none" }} />

          <input
            type="text"
            placeholder="Email"
            className="w-4/5 px-4 py-3 mb-4 rounded border border-gray-700 bg-transparent placeholder-gray-400"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="nope"
            name="email-field"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />

          <input
            type="password"
            placeholder="Mật khẩu"
            className="w-4/5 px-4 py-3 mb-4 rounded border border-gray-700 bg-transparent placeholder-gray-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            name="password-field"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />

          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

          <button
            type="submit"
            className="w-4/5 py-3 rounded-full bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm cursor-pointer transition duration-100"
          >
            Đăng nhập
          </button>
        </form>

        <div className="w-full flex flex-col items-center">
          <div className="text-sm text-gray-400 mt-4">
            Chưa có tài khoản?{" "}
            <a href="/register" className="text-blue-400 hover:underline cursor-pointer">
              Đăng ký {">"}
            </a>
          </div>
        </div>
      </div>

      <RightSideLogin />
    </div>
  );
}

export default Login;

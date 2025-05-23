"use client";

import { useRef, useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import RightSideLogin from "../components/RightSideLogin";
import GoogleLoginButton from "../components/GoogleLoginButton";

function Register() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const hasNavigated = useRef(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState(null);

  const validateUsername = (username) => {
    const alphanumericRegex = /^[a-zA-Z0-9]+$/;
    return alphanumericRegex.test(username);
  };

  useEffect(() => {
    const storedUser = sessionStorage.getItem("user");
    if (storedUser && !user) {
      setUser(JSON.parse(storedUser));
    }
  }, [setUser, user]);

  useEffect(() => {
    console.log("Register useEffect: user =", user);
    if (user && !hasNavigated.current) {
      hasNavigated.current = true;
      navigate("/home");
    }
  }, [user, navigate]);

  const handleGoogleLoginSuccess = (userData) => {
    const userEmail = userData.email;
    if (user?.name !== userEmail) {
      setUser({ name: userEmail });
      sessionStorage.setItem("user", JSON.stringify({ name: userEmail }));
    }
    console.log("User email:", userEmail);
  };

  const handleGoogleLoginError = (error) => {
    alert("Login failed. Please try again.");
    console.error("Login failed:", error);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    if (!validateUsername(username)) {
      setError("Tên tài khoản chỉ được chứa chữ cái và số");
      return;
    }

    if (password !== confirmPassword) {
      setError("Mật khẩu xác nhận không khớp");
      return;
    }

    try {
      const response = await fetch("http://localhost:3000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password, name }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Đăng ký thất bại");
      }

      setUser({ username: data.user.username, name: data.user.name });
      sessionStorage.setItem(
        "user",
        JSON.stringify({ username: data.user.username, name: data.user.name })
      );
      console.log("Đăng ký thành công:", data.user);
    } catch (error) {
      setError(error.message);
      console.error("Lỗi đăng ký:", error.message);
    }
  };

  const inputClassName =
    "w-4/5 px-4 py-3 mb-4 rounded border border-gray-700 bg-transparent placeholder-gray-400";

  return (
    <div className="flex min-h-screen text-white bg-black">
      {/* Left side */}
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
        <form
          onSubmit={handleRegister}
          className="w-full flex flex-col items-center"
        >
          {/* Hidden dummy inputs to confuse browsers */}
          <input type="text" style={{ display: "none" }} />
          <input type="password" style={{ display: "none" }} />

          <input
            type="text"
            placeholder="Tên tài khoản"
            className={inputClassName}
            value={username}
            onChange={(e) => {
              const value = e.target.value;
              setUsername(value);
              if (
                error === "Tên tài khoản chỉ được chứa chữ cái và số" &&
                validateUsername(value)
              ) {
                setError(null);
              }
            }}
            required
            autoComplete="nope"
            name="reg-username"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />
          <input
            type="text"
            placeholder="Họ và tên"
            className={inputClassName}
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            autoComplete="nope"
            name="reg-fullname"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />
          <input
            type="password"
            placeholder="Mật khẩu"
            className={inputClassName}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            name="reg-password"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />
          <input
            type="password"
            placeholder="Xác nhận mật khẩu"
            className={inputClassName}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            autoComplete="new-password"
            name="reg-confirm-password"
            readOnly
            onFocus={(e) => e.target.removeAttribute("readonly")}
          />
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <button
            type="submit"
            className="w-4/5 py-3 rounded-full bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm cursor-pointer transition duration-100"
          >
            Đăng ký
          </button>
        </form>
        <div className="w-full flex flex-col items-center">
          <div className="text-sm text-gray-400 mt-4">
            Đã có tài khoản?{" "}
            <a
              href="/login"
              className="text-blue-400 hover:underline cursor-pointer"
            >
              Đăng nhập {">"}
            </a>
          </div>
        </div>
      </div>
      {/* Right side */}
      <RightSideLogin />
    </div>
  );
}

export default Register;

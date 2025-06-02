import { useRef, useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import RightSideLogin from "../components/RightSideLogin";
import GoogleLoginButton from "../components/GoogleLoginButton";
import images from "../assets/images";

function Login() {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const hasNavigated = useRef(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const storedUser = sessionStorage.getItem("user");
    if (storedUser && !user) {
      setUser(JSON.parse(storedUser));
    }
  }, [setUser, user]);

  useEffect(() => {
    console.log("Login useEffect: user =", user);
    if (user && !hasNavigated.current) {
      hasNavigated.current = true;
      navigate("/home");
    }
  }, [user, navigate]);

  // Handle Google login success
  const handleGoogleLoginSuccess = (dataFromBackend) => {
    console.log("Google login backend response:", dataFromBackend);
    // dataFromBackend có thể chứa user info hoặc token riêng của backend
    // Lưu user info vào context/sessionStorage
    if (dataFromBackend && dataFromBackend.user) {
      setUser(dataFromBackend.user);
      sessionStorage.setItem("user", JSON.stringify(dataFromBackend.user));
    }
  };

  // Handle Google login error
  const handleGoogleLoginError = (error) => {
    alert("Login failed. Please try again.");
    console.error("Login failed:", error);
  };

  // Handle username/password login
  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch("http://localhost:3000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Đăng nhập thất bại");
      }

      // Lưu thông tin người dùng vào AuthContext và sessionStorage
      setUser({ name: data.user.name, username: data.user.username });
      sessionStorage.setItem(
        "user",
        JSON.stringify({ name: data.user.name, username: data.user.username })
      );
      console.log("Đăng nhập thành công:", data.user);
    } catch (error) {
      setError(error.message);
      console.error("Lỗi đăng nhập:", error.message);
    }
  };

  return (
    <div className="flex min-h-screen text-white bg-black">
      {/* Left side */}
      <div className="w-4/10 flex flex-col justify-center px-12">
        <div className="flex items-center mb-8">
          <img
            className="w-10 h-10 rounded-full mr-2"
            src={images.logoAI}
            alt="AIGen logo"
          />
          <p className="text-4xl font-semibold pl-2 pb-1.5">AIGen</p>
        </div>

        <h1 className="text-4xl font-bold mb-6">
          Chào mừng đến với{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
            AIGen
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
          onSubmit={handleLogin}
          className="w-full flex flex-col items-center"
        >
          <input type="text" style={{ display: "none" }} />
          <input type="password" style={{ display: "none" }} />

          <input
            type="text"
            placeholder="Tên tài khoản"
            className="w-4/5 px-4 py-3 mb-4 rounded border border-gray-700 bg-transparent placeholder-gray-400"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoComplete="nope"
            name="username-field"
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
            <a
              href="/register"
              className="text-blue-400 hover:underline cursor-pointer"
            >
              Đăng ký {">"}
            </a>
          </div>
        </div>
      </div>
      {/* Right side */}
      <RightSideLogin />
    </div>
  );
}

export default Login;

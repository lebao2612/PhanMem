import React from "react";
import { useGoogleLogin } from "@react-oauth/google";

const GoogleLoginButton = ({
  onSuccess,
  onError,
  buttonText = "Tham gia bằng Google",
}) => {
  const handleLoginGG = async (credentialResponse) => {
    try {
      // Lấy thông tin người dùng từ Google
      const res = await fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
        headers: {
          Authorization: `Bearer ${credentialResponse.access_token}`,
        },
      });
      const userData = await res.json();
      console.log("Dữ liệu người dùng từ GG:", userData);

      // Gửi token lên backend của bạn
      const backendRes = await fetch("http://localhost:3000/api/auth/google", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          accessToken: credentialResponse.access_token,
          profile: userData,
        }),
      });

      const data = await backendRes.json();

      if (!backendRes.ok) {
        throw new Error("Xác thực Google không thành công");
      }

      sessionStorage.setItem("access_token", data.token);

      onSuccess(data);
    } catch (error) {
      if (onError) {
        onError(error);
      } else {
        alert("Login failed. Please try again.");
        console.error("Login failed:", error);
      }
    }
  };

  const handleErrorGG = (error) => {
    if (onError) {
      onError(error);
    } else {
      alert("Login failed. Please try again.");
      console.error("Login failed:", error);
    }
  };

  const loginAccess = useGoogleLogin({
    onSuccess: handleLoginGG,
    onError: handleErrorGG,
    useOneTap: true,
    scope: "profile email",
  });

  return (
    <button
      className="flex items-center justify-center w-4/5 bg-[#1c1c1c] rounded-full py-3 mb-3 border border-[#333] hover:bg-[#333] transition duration-100 cursor-pointer"
      onClick={() => loginAccess()}
      type="button"
    >
      <img
        src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg"
        className="w-5 h-5 mr-2"
        alt="Google"
      />
      {buttonText}
    </button>
  );
};

export default GoogleLoginButton;

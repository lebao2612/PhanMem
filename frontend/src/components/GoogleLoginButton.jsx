import React from "react";
import { useGoogleLogin } from "@react-oauth/google";

const GoogleLoginButton = ({
  onSuccess,
  onError,
  buttonText = "Tham gia bằng Google",
}) => {
  const handleLoginGG = async (credentialResponse) => {
    try {
      const res = await fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
        headers: {
          Authorization: `Bearer ${credentialResponse.access_token}`,
        },
      });
      const userData = await res.json();
      onSuccess(userData);
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

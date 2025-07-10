"use client";

// Phiên bản thay thế với gradient xanh giống nút chính
const GoogleLoginButtonAlternative = ({
  buttonText = "Sign in with Google",
}) => {
  const handleGoogleLogin = () => {
    window.location.href = "/api/auth/google/oauth";
  };

  return (
    <button
      className="flex items-center justify-center w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-medium rounded-full py-3 mb-3 transition-all duration-200 cursor-pointer shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
      onClick={handleGoogleLogin}
      type="button"
    >
      <img
        src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg"
        className="w-5 h-5 mr-3"
        alt="Google"
      />
      {buttonText}
    </button>
  );
};

export default GoogleLoginButtonAlternative;

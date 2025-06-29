const GoogleLoginButton = ({ buttonText = "Đăng nhập bằng Google" }) => {
  const handleGoogleLogin = () => {
    window.location.href = "/api/auth/google/oauth";
  };

  return (
    <button
      className="flex items-center justify-center w-[400px] w-4/5 bg-[#1c1c1c] rounded-full py-3 mb-3 border border-[#333] hover:bg-[#333] transition duration-100 cursor-pointer"
      onClick={handleGoogleLogin}
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

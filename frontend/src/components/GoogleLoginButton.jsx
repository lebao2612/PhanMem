const GoogleLoginButton = ({ buttonText = "Đăng nhập bằng Google" }) => {
  const handleGoogleLogin = async () => {
    // window.location.href = "/api/auth/google/oauth";
    try {
      const response = await fetch("/api/auth/google/oauth", {
        method: "GET",
        redirect: "manual", // tránh browser auto redirect
      });

      if (response.status === 307 || response.status === 302) {
        const redirectUrl = response.headers.get("Location");
        if (redirectUrl) {
          window.location.href = redirectUrl;
        } else {
          alert("Không lấy được đường dẫn redirect từ Google.");
        }
      } else {
        const text = await response.text();
        alert("Có lỗi xảy ra khi xử lý Google OAuth:\n" + text);
      }
    } catch (error) {
      console.error("Google login error:", error);
      alert("Lỗi kết nối đến máy chủ. Vui lòng thử lại sau.");
    }
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

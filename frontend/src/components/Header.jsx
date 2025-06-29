import images from "../assets/images";
import { useContext, useState } from "react";
import { AuthContext } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  // Handle logout
  const handleLogout = () => {
    setUser(null);
    sessionStorage.removeItem("user");
    navigate("/login");
  };

  const getDisplayInitial = () => {
    if (!user?.name) return null;
    if (user.name.includes("@")) {
      return user.name.split("@")[0]?.charAt(0)?.toUpperCase();
    }
    return user.name.charAt(0)?.toUpperCase();
  };

  return (
    <div>
      {/* Top Navigation */}
      <div className="h-16 border-b border-zinc-800 flex justify-between px-4">
        <div
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => window.location.reload()}
        >
          <img
            src={images.logoAI}
            alt="logo"
            className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center"
          />
          <span className="font-semibold text-lg">AIGen</span>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-1 bg-transparent text-sm border border-zinc-700 rounded-full px-3 py-1 hover:bg-zinc-700 transition-colors cursor-pointer"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-red-400"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            <span>Logout</span>
          </button>
          <div className="h-8 w-8 rounded-full overflow-hidden border border-zinc-700 bg-zinc-800 flex items-center justify-center">
            {getDisplayInitial() || <i className="fa-solid fa-user"></i>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;

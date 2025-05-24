import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../contexts/AuthContext";
import images from "../assets/images";
import { handlePressMenu, countInputWord } from "../scripts/home";

const Home = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [wordCount, setWordCount] = useState(0);
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  console.log("Home: user =", user);

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
    <div className="relative flex h-screen bg-black text-white">
      {/* Overlay */}
      {menuOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          onClick={handlePressMenu(menuOpen, setMenuOpen)}
        ></div>
      )}

      {/* Left Sidebar */}
      <div className={`w-16 border-r border-zinc-800 flex flex-col items-center py-4 ${menuOpen ? 'z-50' : ''}`}>
        <button
          className="fa-solid fa-bars hover:bg-zinc-400 cursor-pointer p-2 rounded-sm"
          onClick={handlePressMenu(menuOpen, setMenuOpen)}
        ></button>
      </div>

      {/* Main Content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ${menuOpen ? 'blur-sm' : ''}`}>
        {/* Top Navigation */}
        <div className="h-16 border-b border-zinc-800 flex justify-between px-4">
          <div className="flex items-center gap-2">
            <img src={images.logoAI} alt="logo" className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center" />
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

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col items-center justify-start pt-8 px-4 overflow-y-auto">
          {/* Version Selector */}
          <div className="mb-6">
            <button className="flex items-center gap-2 bg-zinc-800/50 hover:bg-zinc-800 text-sm rounded-md px-3 py-1.5 transition-colors">
              <span>v3.0</span>
              <i className="fa-solid fa-angle-down"></i>
            </button>
          </div>

          {/* Text Input Area */}
          <div className="w-full max-w-3xl bg-zinc-900 rounded-xl border border-zinc-800 overflow-hidden">
            <div className="min-h-[280px] p-6">
              <textarea
                placeholder="Give me a topic, premise and detailed instructions in any language"
                className="w-full h-full min-h-[200px] bg-transparent border-none outline-none resize-none text-zinc-400 placeholder:text-zinc-500"
                onChange={countInputWord(setWordCount)}
              />
            </div>
            <div className="flex items-center justify-between p-4 border-t border-zinc-800">
              <div className="text-xs text-zinc-500"> {wordCount}/32000 </div>
              <button className="bg-blue-600 hover:bg-blue-700 cursor-pointer text-white rounded-md px-4 py-2 flex items-center gap-2 transition-colors">
                <span>Generate a video</span>
              </button>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap justify-center gap-3 mt-8 max-w-3xl">
            <button className="flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors">
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
                className="text-orange-400"
              >
                <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18" />
                <path d="M10 8V16" />
                <path d="M14 8V16" />
              </svg>
              <span>Create short video</span>
            </button>
            <button className="flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors">
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
                className="text-teal-400"
              >
                <path d="M2 3h20" />
                <path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3" />
                <path d="m7 16 5 5 5-5" />
              </svg>
              <span>Make explainer video</span>
            </button>
            <button className="flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors">
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
                className="text-purple-400"
              >
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
                <path d="m9 15 3-3 3 3" />
                <path d="M9 18h6" />
              </svg>
              <span>Create animated film</span>
            </button>
            <button className="flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors">
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
                className="text-blue-400"
              >
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" x2="8" y1="13" y2="13" />
                <line x1="16" x2="8" y1="17" y2="17" />
                <line x1="10" x2="8" y1="9" y2="9" />
              </svg>
              <span>Use my script</span>
            </button>
          </div>
          {/* Footer */}
          <div className="mt-auto py-4 text-xs text-zinc-500">
            invideo AI can make mistakes. Check important info.
          </div>
        </div>
      </div>

      {/* Side Menu */}
      <div
        className={`fixed top-0 left-0 z-50 h-full bg-neutral-900 flex transition-transform duration-300 ease-in-out ${
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="border border-zinc-800 items-center">
          <div className="p-4 flex gap-8 items-center">
            <button
              className="fa-solid fa-bars hover:bg-zinc-400 cursor-pointer p-2 rounded-sm"
              onClick={handlePressMenu(menuOpen, setMenuOpen)}
            ></button>
            <div className="flex items-center gap-2 px-4">
              <img src={images.logoAI} alt="logo" className="h-8 w-8 rounded-full bg-blue-500" />
              <span className="font-semibold text-lg">AIGen</span>
            </div>
          </div>
          <ul className="gap-2 flex flex-col px-4 mt-2">
            <li className="hover:bg-neutral-500 cursor-pointer p-2 rounded-sm">
              <i className="fa-solid fa-square-poll-horizontal mr-2 text-2xl"></i>
              Dashboard
            </li>
            <li className="hover:bg-neutral-500 cursor-pointer p-2 rounded-sm">
              <i className="fa-solid fa-gears mr-2 text-2xl"></i>
              Settings
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Home;
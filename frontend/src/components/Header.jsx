"use client"

import { useContext, useState } from "react"
import { AuthContext } from "../contexts/AuthContext"
import { useNavigate } from "react-router-dom"
import images from "../assets/images"
import Settings from "./Setting"

const Header = () => {
  const { user, setUser } = useContext(AuthContext)
  const navigate = useNavigate()
  const [showPopup, setShowPopup] = useState(false)
  const [showSettingsOverlay, setShowSettingsOverlay] = useState(false)

  // Handle logout
  const handleLogout = () => {
    setUser(null)
    sessionStorage.removeItem("user")
    sessionStorage.removeItem("token")
    navigate("/login")
    setShowPopup(false)
  }

  const handleSettings = () => {
    setShowSettingsOverlay(true)
    setShowPopup(false)
  }

  const getDisplayInitial = () => {
    if (!user?.name) return null
    if (user.name.includes("@")) {
      return user.name.split("@")[0]?.charAt(0)?.toUpperCase()
    }
    return user.name.charAt(0)?.toUpperCase()
  }

  return (
    <div>
      {/* Top Navigation */}
      <div className="h-16 border-b border-zinc-800 flex justify-between px-4">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => window.location.reload()}>
          <img
            src={images.logoAI || "/placeholder.svg"}
            alt="logo"
            className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center"
          />
          <span className="font-semibold text-lg">AIGen</span>
        </div>
        <div className="flex items-center gap-4">
          {/* User Avatar with Popup */}
          <div className="relative">
            <div
              className="cursor-pointer h-8 w-8 rounded-full overflow-hidden border border-zinc-700 bg-zinc-800 flex items-center justify-center text-white text-sm font-semibold"
              onClick={() => setShowPopup(!showPopup)}
            >
              {user?.picture ? (
                <img src={user.picture || "/placeholder.svg"} alt="avatar" className="w-full h-full object-cover" />
              ) : (
                getDisplayInitial() || <i className="fa-solid fa-user" />
              )}
            </div>

            {/* Popup Menu */}
            {showPopup && (
              <div className="absolute right-0 top-10 bg-zinc-800 border border-zinc-700 rounded-lg shadow-lg py-2 w-32 z-50">
                <button
                  onClick={handleSettings}
                  className="w-full text-left px-4 py-2 text-sm text-white hover:bg-zinc-700 transition-colors flex items-center gap-2"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="3" />
                    <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1" />
                  </svg>
                  Settings
                </button>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-zinc-700 transition-colors flex items-center gap-2"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" y1="12" x2="9" y2="12" />
                  </svg>
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Overlay to close popup when clicking outside */}
      {showPopup && <div className="fixed inset-0 z-40" onClick={() => setShowPopup(false)} />}

      {/* Settings Component */}
      <Settings isOpen={showSettingsOverlay} onClose={() => setShowSettingsOverlay(false)} />
    </div>
  )
}

export default Header

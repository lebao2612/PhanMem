"use client"

import { useContext, useState, useEffect } from "react"
import { AuthContext } from "../contexts/AuthContext"
import { useNavigate } from "react-router-dom"
import images from "../assets/images"

const SettingsContent = () => {
  const [settings, setSettings] = useState({
    theme: "dark",
    language: "en",
    voiceGender: "female",
    styles: [],
  })
  const [isLoading, setIsLoading] = useState(false)
  const [saveMessage, setSaveMessage] = useState("")

  useEffect(() => {
    const mockSettingsFromDB = {
      theme: "light",
      language: "vi",
      voiceGender: "male",
      styles: ["Hóm hỉnh", "Khích lệ"],
    }
    setSettings(mockSettingsFromDB)
  }, [])

  const handleSettingChange = (key, value) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }))
  }

  const handleSave = async () => {
    console.log("save click")
  }

  const handleReset = () => {
    const defaultSettings = {
      theme: "dark",
      language: "en",
      voiceGender: "female",
      styles: [],
    }
    setSettings(defaultSettings)
  }

  const settingsConfig = [
    {
      key: "theme",
      label: "Theme",
      type: "select",
      options: [
        { value: "dark", label: "Dark" },
        { value: "light", label: "Light" },
        { value: "auto", label: "Auto" },
      ],
    },
    {
      key: "language",
      label: "Language",
      type: "select",
      options: [
        { value: "en", label: "English" },
        { value: "vi", label: "Tiếng Việt" },
        { value: "zh", label: "中文" },
        { value: "ja", label: "日本語" },
        { value: "ko", label: "한국어" },
      ],
    },
    {
      key: "voiceGender",
      label: "Voice Gender",
      type: "select",
      options: [
        { value: "female", label: "Female" },
        { value: "male", label: "Male" },
        { value: "neutral", label: "Neutral" },
      ],
    },
  ]

  const personalityOptions = [
    "Hoạt ngôn",
    "Hóm hỉnh",
    "Thẳng thắn",
    "Khích lệ",
    "Phong cách Gen Z",
    "Hoài nghi",
    "Truyền thống",
    "Tư tưởng tân tiến",
    "Thơ mộng",
  ]

  return (
    <div className="p-6">
      {/* Save Message */}
      {saveMessage && (
        <div
          className={`mb-6 p-4 rounded-lg ${
            saveMessage.includes("successfully")
              ? "bg-green-900/20 border border-green-500/30 text-green-400"
              : "bg-red-900/20 border border-red-500/30 text-red-400"
          }`}
        >
          {saveMessage}
        </div>
      )}

      {/* Settings Form */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <div className="grid gap-6 md:grid-cols-2">
          {settingsConfig.map((config) => (
            <div key={config.key} className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">{config.label}</label>
              {config.type === "select" && (
                <select
                  value={settings[config.key]}
                  onChange={(e) => handleSettingChange(config.key, e.target.value)}
                  className="cursor-pointer w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {config.options?.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              )}
            </div>
          ))}
        </div>

        {/* Personality Style Selector */}
        <div className="mt-8">
          <label className="block text-sm font-medium text-gray-300 mb-2">Phong cách</label>
          <div className="flex flex-wrap gap-3">
            {personalityOptions.map((style) => {
              const selected = settings.styles.includes(style)
              return (
                <button
                  key={style}
                  onClick={() => {
                    setSettings((prev) => ({
                      ...prev,
                      styles: selected ? prev.styles.filter((s) => s !== style) : [...prev.styles, style],
                    }))
                  }}
                  className={`cursor-pointer px-4 py-2 rounded-full border text-sm transition-all duration-200 ${
                    selected
                      ? "bg-blue-600 text-white border-blue-500"
                      : "bg-transparent text-gray-400 border-gray-600 hover:bg-gray-700"
                  }`}
                >
                  {style}
                </button>
              )
            })}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4 mt-8 pt-6 border-t border-gray-700">
          <button
            onClick={handleReset}
            className="cursor-pointer px-6 py-2 text-gray-400 hover:text-white border border-gray-600 hover:border-gray-500 rounded-lg transition-all duration-200"
          >
            Reset to Default
          </button>
          <button
            onClick={handleSave}
            disabled={isLoading}
            className="cursor-pointer px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
          >
            {isLoading && (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            )}
            <span>{isLoading ? "Saving..." : "Save Settings"}</span>
          </button>
        </div>
      </div>
    </div>
  )
}

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
          {/* <button
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
          </button> */}

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

      {/* Settings Overlay */}
      {showSettingsOverlay && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
            {/* Settings Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-800">
              <div>
                <h1 className="text-2xl font-bold text-white">Settings</h1>
                <p className="text-gray-400">Customize your application preferences</p>
              </div>
              <button
                onClick={() => setShowSettingsOverlay(false)}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>

            {/* Settings Content */}
            <SettingsContent />
          </div>
        </div>
      )}
    </div>
  )
}

export default Header

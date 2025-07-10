"use client"

import { useEffect, useState } from "react"
import Header from "../components/Header"
import LeftSideBar from "../components/LeftSideBar"

const Setting = () => {
  const [settings, setSettings] = useState({
    theme: "dark",
    language: "en",
    voiceGender: "female",
    styles: [], // Thêm field mới
  })

  const [isLoading, setIsLoading] = useState(false)
  const [saveMessage, setSaveMessage] = useState("")

  // Load settings from localStorage or mockDB
  useEffect(() => {
    const mockSettingsFromDB = {
      theme: "light",
      language: "vi",
      voiceGender: "male",
      styles: ["Hóm hỉnh", "Khích lệ"], // ví dụ có sẵn
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
    // setIsLoading(true)
    // try {
    //   const response = await fetch("/api/settings", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(settings),
    //   })
    //   if (!response.ok) throw new Error("Failed to save to database")
    //   setSaveMessage("Settings saved successfully!")
    // } catch (error) {
    //   console.error("Save error:", error)
    //   setSaveMessage("Failed to save settings. Please try again.")
    // } finally {
    //   setIsLoading(false)
    //   setTimeout(() => setSaveMessage(""), 3000)
    // }
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
    <div className="relative flex h-screen bg-black text-white">
      <LeftSideBar />
      <div className="flex-1 flex flex-col transition-all duration-300">
        <Header />

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
              <p className="text-gray-400">Customize your application preferences</p>
            </div>

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
            <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
              <div className="grid gap-6 md:grid-cols-2">
                {settingsConfig.map((config) => (
                  <div key={config.key} className="space-y-2">
                    <label className="block text-sm font-medium text-gray-300">{config.label}</label>

                    {config.type === "select" && (
                      <select
                        value={settings[config.key]}
                        onChange={(e) => handleSettingChange(config.key, e.target.value)}
                        className="cursor-pointer w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
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
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Phong cách
                </label>
                <div className="flex flex-wrap gap-3">
                  {personalityOptions.map((style) => {
                    const selected = settings.styles.includes(style)
                    return (
                      <button
                        key={style}
                        onClick={() => {
                          setSettings((prev) => ({
                            ...prev,
                            styles: selected
                              ? prev.styles.filter((s) => s !== style)
                              : [...prev.styles, style],
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
              <div className="flex justify-end space-x-4 mt-8 pt-6 border-t border-gray-800">
                <button
                  onClick={handleReset}
                  className="cursor-pointer px-6 py-2 text-gray-400 hover:text-white border border-gray-700 hover:border-gray-600 rounded-lg transition-all duration-200"
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
        </div>
      </div>
    </div>
  )
}

export default Setting

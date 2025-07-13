"use client"

import { useState, useEffect, useContext } from "react"
import { AuthContext } from "../contexts/AuthContext";

const Settings = ({ isOpen, onClose }) => {
    const [settings, setSettings] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const [saveMessage, setSaveMessage] = useState("")
    
    const { authFetch } = useContext(AuthContext);

    //const userInfo = JSON.parse(sessionStorage.getItem("user"));

    //const userSetting = userInfo.settings

    

    useEffect(() => {
        const userStr = sessionStorage.getItem("user")
        if (userStr) {
            const userInfo = JSON.parse(userStr)
            if (userInfo.settings) {
                setSettings(userInfo.settings)
            }
        }
    }, [])

    const handleSettingChange = (key, value) => {
        setSettings((prev) => ({
        ...prev,
        [key]: value,
        }))
    }

    console.log(settings)

    const handleSave = async () => {
        setIsLoading(true)
        setSaveMessage("")

        
        const allowedSettings = {
            language: settings.language,
            voiceGender: settings.voiceGender,
            LLMModel: settings.LLMModel,
            personality: settings.personality,
        }

        console.log(allowedSettings)

        try {
            const responseData = await authFetch(`/api/users/settings`, {
                method: "PATCH",
                body: JSON.stringify(allowedSettings),
            })

            sessionStorage.setItem("user", JSON.stringify(responseData.data))
            setSaveMessage("Settings saved successfully!")
        } catch (error) {
            console.error(error)
            setSaveMessage("Something went wrong. Please try again.")
        } finally {
            setIsLoading(false)
        }
    }


    const handleReset = () => {
        const defaultSettings = {
        language: "vi",
        llm_model: "gemini-1.5-flash",
        voice_gender: "female",
        personality: [],
        }
        setSettings(defaultSettings)
    }

    const settingsConfig = [
        {
        key: "language",
        label: "Language",
        type: "select",
        options: [
            { value: "en", label: "English" },
            { value: "vi", label: "Tiếng Việt" },
        ],
        },
        {
        key: "voice_gender",
        label: "Voice Gender",
        type: "select",
        options: [
            { value: "female", label: "Female" },
            { value: "male", label: "Male" },
        ],
        },
        {
            key: "llm_model",
            label: "LLM Model",
            type: "select",
            options: [
                {value: "gemini-1.5-flash", label: "Gemini 1.5 Flash"},
                {value: "gemini-1.5-pro", label: "Gemini 1.5 Pro"},
            ]
        }
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

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-gray-900 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
                {/* Settings Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-800">
                <div>
                    <h1 className="text-2xl font-bold text-white">Settings</h1>
                    <p className="text-gray-400">Customize your application preferences</p>
                </div>
                <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
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
                        <label className="block text-sm font-medium text-gray-300 mb-2">Personality</label>
                        <div className="flex flex-wrap gap-3">
                            {personalityOptions.map((style) => {
                            const selected = settings.personality.includes(style)
                            return (
                                <button
                                key={style}
                                onClick={() => {
                                    setSettings((prev) => ({
                                    ...prev,
                                    personality: selected ? prev.personality.filter((s) => s !== style) : [...prev.personality, style],
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
            </div>
        </div>
    )
}

export default Settings

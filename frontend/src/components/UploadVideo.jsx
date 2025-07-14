"use client"
import { useContext, useState, useEffect } from "react"
import { ArrowLeft } from "lucide-react"
import { AuthContext } from "../contexts/AuthContext"

function UploadVideo({ selectedVideo, onClose, onBack, onSuccess }) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [category, setCategory] = useState("22")
  const [privacy, setPrivacy] = useState("private")
  const [loading, setLoading] = useState(false)
  const { authFetch } = useContext(AuthContext)

  useEffect(() => {
    console.log("selectedVideo for upload:", selectedVideo)
    if (selectedVideo) {
      setTitle(selectedVideo.title || "")
      setDescription(selectedVideo.description || "")
    }
  }, [selectedVideo])

  const handleUpload = async () => {
    setLoading(true)
    console.log("Attempting upload:", {
      title,
      description,
      category,
      privacy,
    })

    if (!selectedVideo?.id || !title || !description) {
      alert("Thiếu thông tin video.")
      setLoading(false)
      return
    }

    try {
      const responseData = await authFetch(`/api/videos/youtube/upload/${selectedVideo.id}`, {
        method: "POST",
        body: JSON.stringify({
          title,
          description,
          category,
          privacy,
          exportData: selectedVideo.exportData,
        }),
      })
      onClose()
      if (onSuccess) {
        onSuccess()
      }
    } catch (error) {
      console.error("Error uploading video:", error)
      alert("Đã xảy ra lỗi khi upload video.")
    }
    window.location.reload()
    setLoading(false)
  }

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 text-white">
      {/* Header */}
      <div className="flex items-center gap-4 p-6 border-b border-zinc-700/50 bg-zinc-800/50 backdrop-blur-sm">
        <button
          onClick={onBack || onClose}
          className="flex items-center justify-center w-10 h-10 bg-zinc-700/60 hover:bg-zinc-600/80 rounded-xl transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          Upload to YouTube
        </h2>
      </div>

      {/* Form Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Video Title */}
        <div className="space-y-2">
          <label className="block text-sm font-semibold text-zinc-300 tracking-wide">Video Title</label>
          <input
            type="text"
            placeholder="Enter your video title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-800/60 text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:bg-zinc-800/80 text-sm border border-zinc-700/50 transition-all duration-200 hover:border-zinc-600/50"
          />
        </div>

        {/* Description */}
        <div className="space-y-2">
          <label className="block text-sm font-semibold text-zinc-300 tracking-wide">Description</label>
          <textarea
            placeholder="Describe your video content..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
            className="w-full px-4 py-3.5 rounded-xl bg-zinc-800/60 text-white placeholder-zinc-400 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:bg-zinc-800/80 text-sm border border-zinc-700/50 transition-all duration-200 hover:border-zinc-600/50"
          />
        </div>

        {/* Category and Privacy Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Category */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-zinc-300 tracking-wide">Category</label>
            <div className="relative">
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-3.5 rounded-xl bg-zinc-800/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:bg-zinc-800/80 text-sm border border-zinc-700/50 appearance-none cursor-pointer transition-all duration-200 hover:border-zinc-600/50"
              >
                <option value="22">People & Blogs</option>
                <option value="24">Entertainment</option>
                <option value="10">Music</option>
                <option value="15">Pets & Animals</option>
                <option value="17">Sports</option>
                <option value="19">Travel & Events</option>
                <option value="20">Gaming</option>
                <option value="26">Howto & Style</option>
                <option value="27">Education</option>
                <option value="28">Science & Technology</option>
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg className="w-4 h-4 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          {/* Privacy */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-zinc-300 tracking-wide">Privacy</label>
            <div className="relative">
              <select
                value={privacy}
                onChange={(e) => setPrivacy(e.target.value)}
                className="w-full px-4 py-3.5 rounded-xl bg-zinc-800/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:bg-zinc-800/80 text-sm border border-zinc-700/50 appearance-none cursor-pointer transition-all duration-200 hover:border-zinc-600/50"
              >
                <option value="private">Private</option>
                <option value="public">Public</option>
                <option value="unlisted">Unlisted</option>
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg className="w-4 h-4 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Button */}
      <div className="p-6 border-t border-zinc-700/50 bg-zinc-800/30 backdrop-blur-sm">
        <button
          onClick={handleUpload}
          disabled={loading}
          className={`w-full py-4 px-6 rounded-xl font-semibold transition-all duration-300 shadow-lg text-base relative overflow-hidden group ${
            loading
              ? "bg-zinc-700/50 text-zinc-400 cursor-not-allowed"
              : "bg-gradient-to-r from-purple-600 via-purple-500 to-pink-500 hover:from-purple-700 hover:via-purple-600 hover:to-pink-600 text-white shadow-purple-500/25 hover:shadow-purple-500/40 hover:shadow-lg transform hover:scale-[1.02] active:scale-[0.98]"
          }`}
        >
          {!loading && (
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
          )}
          <span className="relative flex items-center justify-center gap-2">
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin" />
                Uploading...
              </>
            ) : (
              "Upload to YouTube"
            )}
          </span>
        </button>
      </div>
    </div>
  )
}

export default UploadVideo

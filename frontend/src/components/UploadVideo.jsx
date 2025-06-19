"use client"

import { useState, useEffect } from "react"
import { ArrowLeft } from "lucide-react"

function UploadVideo({ selectedVideo, onClose, onBack }) {
  const [videoUrl, setVideoUrl] = useState("") // Thêm state cho videoUrl
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [category, setCategory] = useState("22") // Mặc định: People & Blogs
  const [privacy, setPrivacy] = useState("private")
  const [loading, setLoading] = useState(false)

  // Sử dụng useEffect để populate dữ liệu từ selectedVideo
  useEffect(() => {
    if (selectedVideo) {
      setVideoUrl(selectedVideo.videoURL || selectedVideo.videoID || "")
      setTitle(selectedVideo.name || "")
      setDescription(`Video được tạo ngày ${selectedVideo.date || selectedVideo.createAt || ""}`)
    }
  }, [selectedVideo])

  const handleUpload = async () => {
    setLoading(true)
    if (!videoUrl || !title || !description) {
      alert("Please fill in Video URL, Title, and Description.")
      setLoading(false)
      return
    }

    try {
      console.log("Sending data:", { videoUrl, title, description, category, privacy })
      const response = await fetch("http://localhost:5000/api/upload-video", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          video_url: videoUrl,
          title,
          description,
          category,
          privacy,
        }),
      })

      const result = await response.json()
      console.log("Response:", result)
      if (response.ok) {
        alert("Video uploaded successfully!")
        // Có thể gọi onClose() để đóng form sau khi upload thành công
        if (onClose) onClose()
      } else {
        alert(`Error: ${result.detail || result.error || "Unknown error"}`)
      }
    } catch (error) {
      console.error("Error uploading video:", error)
      alert("Failed to upload video.")
    }
    setLoading(false)
  }

  return (
    <div className="space-y-2 text-white h-full flex flex-col p-1">
        {console.log(videoUrl)}
      {/* Header với nút Back */}
      <div className="flex items-center gap-3 mb-4">
        <button
          onClick={onBack || onClose}
          className="flex items-center justify-center w-8 h-8 bg-zinc-700/50 hover:bg-zinc-600 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <h2 className="text-xl font-bold">Upload to YouTube</h2>
      </div>

      {/* Form fields */}
      <div className="space-y-2 flex-1 overflow-y-auto px-1">
        {/* <div>
          <label className="block text-sm font-medium text-zinc-300 mb-2">Video URL</label>
          <input
            type="text"
            placeholder="Video URL"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-zinc-700 text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm border border-zinc-600"
          />
        </div> */}

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">Video Title</label>
          <input
            type="text"
            placeholder="Video Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-zinc-700 text-white placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm border border-zinc-600"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">Description</label>
          <textarea
            placeholder="Video Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-4 py-3 rounded-lg bg-zinc-700 text-white placeholder-zinc-400 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm border border-zinc-600"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm border border-zinc-600 appearance-none"
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
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">Privacy</label>
          <select
            value={privacy}
            onChange={(e) => setPrivacy(e.target.value)}
            className="mb-2 w-full px-4 py-3 rounded-lg bg-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm border border-zinc-600 appearance-none"
          >
            <option value="private">Private</option>
            <option value="public">Public</option>
            <option value="unlisted">Unlisted</option>
          </select>
        </div>
      </div>

      {/* Upload button */}
      <div className="pt-4 border-t border-zinc-700/50">
        <button
          onClick={handleUpload}
          disabled={loading}
          className={`cursor-pointer w-full py-4 px-6 rounded-lg font-semibold transition-all duration-200 shadow-md text-base ${
            loading
              ? "bg-zinc-600 text-zinc-400 cursor-not-allowed"
              : "bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
          }`}
        >
          {loading ? "Uploading..." : "Upload to YouTube"}
        </button>
      </div>
    </div>
  )
}

export default UploadVideo

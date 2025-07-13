"use client"

import { useState, useEffect, useContext } from "react"
import Header from "../components/Header"
import LeftSideBar from "../components/LeftSideBar"
import { FaYoutube, FaUpload, FaFilm, FaCamera } from "react-icons/fa"
import { X, Calendar, Tag, Download, Upload } from "lucide-react"
import images from "../assets/images"
import { AuthContext } from "../contexts/AuthContext"
import UploadVideo from "../components/UploadVideo"

const Dashboard = () => {
  const options = ["Tất cả", "Youtube"]
  const { authFetch } = useContext(AuthContext)
  const [videos, setVideos] = useState([])
  const [filteredVideo, setFilteredVideo] = useState([])
  console.log(videos)

  const [selectedOption, setSelectedOption] = useState("Tất cả")
  const [selectedVideo, setSelectedVideo] = useState()
  const [selectUpload, setSelectUpload] = useState(false)

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const res = await authFetch("/api/videos/me?limit=20&skip=0")
        setVideos(res)
        setFilteredVideo(res)
      } catch (err) {
        console.error("Lỗi khi gọi API:", err.message)
      }
    }
    fetchVideos()
  }, [authFetch])

  useEffect(() => {
    if (selectedOption === "Tất cả") {
      setFilteredVideo(videos)
    } else {
      setFilteredVideo(videos.filter((video) => video.youtube))
    }
  }, [selectedOption, videos])

  const countYoutubeUploaded = (videos) => {
    return videos.filter((video) => video.youtube).length
  }

  const closeDetailVideo = () => {
    setSelectedVideo(null)
    setSelectUpload(false)
  }

  const downloadVideo = async (url, videoName) => {
    try {
      console.log("Đang tải video...")
      const response = await fetch(url, {
        method: "GET",
        mode: "cors",
        credentials: "omit",
      })
      if (!response.ok) {
        throw new Error(`Không thể tải video: ${response.status} ${response.statusText}`)
      }
      const blob = await response.blob()
      if (!blob.type.startsWith("video/")) {
        throw new Error("Tệp không phải video.")
      }
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = blobUrl
      link.download = videoName.endsWith(".mp4") ? videoName : `${videoName}.mp4`
      link.style.display = "none"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
      console.log("Tải video thành công!")
    } catch (error) {
      console.error("Lỗi khi tải video:", error.message)
      window.open(url, "_blank")
      alert('Không thể tự động tải. Video đã mở trong tab mới. Click chuột phải và chọn "Lưu video dưới dạng" để tải.')
    }
  }

  return (
    <div className="relative flex bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white min-h-screen">
      <LeftSideBar />
      {/* Main Content */}
      <div className={"flex-1 flex flex-col transition-all duration-300"}>
        <Header />

        {/* Enhanced Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 px-6 py-8">
          <div className="group relative overflow-hidden border border-zinc-700/50 bg-gradient-to-br from-purple-900/20 via-zinc-900 to-zinc-800 p-6 shadow-2xl rounded-2xl hover:shadow-purple-500/10 transition-all duration-500 hover:scale-[1.02] hover:border-purple-500/30">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600/5 to-pink-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-purple-500/20 rounded-full blur-xl"></div>
                  <FaFilm className="relative text-purple-400 text-4xl p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl border border-purple-500/30" />
                </div>
                <div>
                  <h3 className="font-bold text-xl bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    Tổng số Video
                  </h3>
                  <p className="text-gray-400 text-sm">Số lượng video đã tạo</p>
                </div>
              </div>
              <div className="flex items-center gap-3 mt-4">
                <FaCamera className="text-xl text-purple-400" />
                <p className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  {videos.length}
                </p>
              </div>
            </div>
          </div>

          <div className="group relative overflow-hidden border border-zinc-700/50 bg-gradient-to-br from-red-900/20 via-zinc-900 to-zinc-800 p-6 shadow-2xl rounded-2xl hover:shadow-red-500/10 transition-all duration-500 hover:scale-[1.02] hover:border-red-500/30">
            <div className="absolute inset-0 bg-gradient-to-r from-red-600/5 to-orange-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-red-500/20 rounded-full blur-xl"></div>
                  <FaYoutube className="relative text-red-400 text-4xl p-3 bg-gradient-to-br from-red-500/20 to-orange-500/20 rounded-2xl border border-red-500/30" />
                </div>
                <div>
                  <h3 className="font-bold text-xl bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    Youtube
                  </h3>
                  <p className="text-gray-400 text-sm">Số lượng video đã upload lên Youtube</p>
                </div>
              </div>
              <div className="flex items-center gap-3 mt-4">
                <FaUpload className="text-xl text-red-400" />
                <p className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
                  {countYoutubeUploaded(videos)}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Filter Section */}
        <div className="px-6 py-4">
          <div className="inline-flex gap-2 p-2 bg-gradient-to-r from-zinc-800/80 to-zinc-900/80 backdrop-blur-sm rounded-xl border border-zinc-700/50 shadow-lg">
            {options.map((option) => (
              <button
                key={option}
                className={`px-6 py-2 rounded-lg font-medium transition-all duration-300 ${
                  selectedOption === option
                    ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg shadow-purple-500/25 scale-105"
                    : "text-gray-400 hover:text-white hover:bg-zinc-700/50"
                }`}
                onClick={() => setSelectedOption(option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>

        {/* Enhanced Video Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-6 py-6">
          {filteredVideo.map((video, index) => (
            <div
              key={index}
              className="group relative bg-gradient-to-br from-zinc-800/80 to-zinc-900/80 backdrop-blur-sm p-5 rounded-2xl shadow-xl border border-zinc-700/50 transform transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/10 cursor-pointer overflow-hidden"
              onClick={() => {
                setSelectedVideo(video)
                console.log(video)
              }}
            >
              {/* Hover Gradient Overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-transparent to-pink-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"></div>

              <div className="relative z-10">
                {/* Video Thumbnail */}
                <div className="relative overflow-hidden rounded-xl mb-4 shadow-lg">
                  <img
                    src={video.thumbnailUrl || "/placeholder.svg"}
                    className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-110"
                    alt="Video thumbnail"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                  {/* Play Button Overlay */}
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                    <div className="bg-white/20 backdrop-blur-sm rounded-full p-4 border border-white/30">
                      <div className="w-0 h-0 border-l-[12px] border-l-white border-y-[8px] border-y-transparent ml-1"></div>
                    </div>
                  </div>
                </div>

                {/* Video Info */}
                <div className="space-y-3">
                  <h3 className="text-lg font-bold line-clamp-2 min-h-[3.5rem] bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent group-hover:from-purple-200 group-hover:to-pink-200 transition-all duration-300">
                    {video.title}
                  </h3>

                  {video.youtube && (
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-2 px-3 py-1 bg-gradient-to-r from-red-500/20 to-orange-500/20 rounded-full border border-red-500/30">
                        <FaYoutube className="text-red-400 text-sm" />
                        <span className="text-xs font-medium text-red-300">YouTube</span>
                      </div>
                    </div>
                  )}

                  {video.youtube && (
                    <a
                      href={video.youtube.videoUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 text-sm transition-colors duration-200 group/link"
                    >
                      <i className="fa-solid fa-link"></i>
                      <span className="group-hover/link:underline">Xem trên YouTube</span>
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Enhanced Modal */}
      {selectedVideo && (
        <>
          {/* Enhanced Backdrop */}
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-md z-40 animate-in fade-in duration-500"
            onClick={closeDetailVideo}
          />

          {/* Enhanced Modal */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-in zoom-in-95 fade-in duration-500">
            <div className="relative bg-gradient-to-br from-zinc-900/95 via-zinc-800/95 to-zinc-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-zinc-700/50 max-w-6xl w-full max-h-[90vh] overflow-hidden">
              {/* Enhanced Close Button */}
              <button
                className="absolute right-6 top-6 z-10 bg-black/40 hover:bg-black/60 text-white border-0 rounded-full p-3 backdrop-blur-sm transition-all duration-300 cursor-pointer hover:scale-110 group"
                onClick={closeDetailVideo}
              >
                <X className="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
              </button>

              {/* Content */}
              <div className="flex flex-col lg:flex-row">
                {/* Enhanced Video Section */}
                <div className="flex-1 w-full p-8 pb-6 lg:pb-8 flex justify-center items-center">
                  <div className="relative w-full rounded-2xl overflow-hidden shadow-2xl border border-zinc-700/50">
                    <video
                      controls
                      className="w-full aspect-video rounded-2xl bg-black"
                      poster="/placeholder.svg?height=400&width=600"
                    >
                      <source src={selectedVideo.url} type="video/mp4" />
                      <source src={selectedVideo.url} type="video/webm" />
                      <source src={selectedVideo.url} type="video/ogg" />
                      Trình duyệt của bạn không hỗ trợ thẻ video.
                    </video>
                  </div>
                </div>

                {/* Enhanced Info Section */}
                <div className="lg:w-96 p-8 pt-6 lg:pt-8 border-t lg:border-t-0 lg:border-l border-zinc-700/50 bg-gradient-to-b from-zinc-800/30 to-zinc-900/30">
                  {selectUpload ? (
                    <UploadVideo
                      selectedVideo={selectedVideo}
                      onClose={closeDetailVideo}
                      onBack={() => setSelectUpload(false)}
                    />
                  ) : (
                    <div className="space-y-8">
                      {/* Enhanced Title */}
                      <div>
                        <h3 className="text-2xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent leading-tight mb-3">
                          {selectedVideo.title}
                        </h3>
                        <div className="w-16 h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 rounded-full shadow-lg shadow-purple-500/30" />
                      </div>

                      {/* Enhanced Metadata */}
                      <div className="space-y-6">
                        <div className="flex items-center gap-4 p-4 bg-gradient-to-r from-zinc-800/50 to-zinc-700/50 rounded-xl border border-zinc-600/30">
                          <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl border border-purple-500/30">
                            <Calendar className="w-5 h-5 text-purple-400" />
                          </div>
                          <div>
                            <p className="text-xs text-zinc-400 uppercase tracking-wider font-semibold">
                              Ngày phát hành
                            </p>
                            <p className="text-sm font-medium text-gray-200">
                              {selectedVideo.createdAt
                                ? new Date(selectedVideo.createdAt).toISOString().slice(0, 10)
                                : "N/A"}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center gap-4 p-4 bg-gradient-to-r from-zinc-800/50 to-zinc-700/50 rounded-xl border border-zinc-600/30">
                          <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl border border-blue-500/30">
                            <Tag className="w-5 h-5 text-blue-400" />
                          </div>
                          <div>
                            <p className="text-xs text-zinc-400 uppercase tracking-wider font-semibold">Xuất bản</p>
                            <span
                              className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold border ${
                                selectedVideo.youtube
                                  ? "bg-gradient-to-r from-red-500/20 to-orange-500/20 text-red-300 border-red-500/30"
                                  : "bg-gradient-to-r from-gray-500/20 to-gray-600/20 text-gray-300 border-gray-500/30"
                              }`}
                            >
                              {selectedVideo.youtube ? "YOUTUBE" : "NONE"}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Enhanced Description */}
                      <div className="p-4 bg-gradient-to-br from-zinc-800/30 to-zinc-900/30 rounded-xl border border-zinc-700/30">
                        <p className="text-sm text-zinc-300 leading-relaxed">
                          Khám phá thế giới tự nhiên qua những thước phim tuyệt đẹp với chất lượng 4K sắc nét.
                        </p>
                      </div>

                      {/* Enhanced Action Buttons */}
                      <div className="space-y-4">
                        <button
                          className="cursor-pointer flex items-center justify-center gap-3 w-full bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 hover:from-purple-600 hover:via-pink-600 hover:to-orange-600 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/30 hover:scale-[1.02] group"
                          onClick={() => downloadVideo(selectedVideo.url || selectedVideo.videoID, selectedVideo.title)}
                        >
                          <Download className="w-5 h-5 group-hover:animate-bounce" />
                          Download Video
                        </button>

                        <button
                          disabled={selectedVideo.youtube}
                          className={`flex items-center justify-center gap-3 w-full border font-semibold py-4 px-6 rounded-xl transition-all duration-300 group ${
                            selectedVideo.youtube
                              ? "bg-zinc-800/50 text-zinc-500 cursor-not-allowed border-zinc-700/50"
                              : "cursor-pointer text-zinc-300 hover:bg-gradient-to-r hover:from-zinc-700/50 hover:to-zinc-600/50 hover:text-white border-zinc-600/50 hover:border-zinc-500/50 hover:scale-[1.02] shadow-lg hover:shadow-xl"
                          }`}
                          onClick={() => setSelectUpload(true)}
                        >
                          <Upload className={`w-5 h-5 ${!selectedVideo.youtube ? "group-hover:animate-bounce" : ""}`} />
                          Upload Video
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard

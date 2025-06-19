import { useState, useEffect } from "react";

function Review({ onClose }) {

  const mockVideo = {videoURL: "https://www.w3schools.com/html/mov_bbb.mp4", user: ""}

  const [platform, setPlatform] = useState("YouTube");
  const [videoData, setVideoData] = useState({ video: "", user: "" });
  const [loadingVideo, setLoadingVideo] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  // useEffect(() => {
  //   fetch("http://localhost:3000/api/video")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setVideoData(data);
  //     })
  //     .catch(console.error)
  //     .finally(() => setLoadingVideo(false));
  // }, []);

  const stopPropagation = (e) => e.stopPropagation();

  // function handleAutoCaption() {
  //   fetch("http://localhost:3000/api/info")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setTitle(data.title || "");
  //       setDescription(data.description || "");
  //     })
  //     .catch(console.error);
  // }

  // function handleDownload() {
  //   if (!videoData.video) {
  //     alert("Không có video để tải.");
  //     return;
  //   }

  //   setIsDownloading(true);

  //   fetch(videoData.video)
  //     .then((res) => res.blob())
  //     .then((blob) => {
  //       const url = window.URL.createObjectURL(blob);
  //       const a = document.createElement("a");
  //       a.href = url;

  //       const cleanTitle = (title || "video")
  //         .replace(/[^a-zA-Z0-9_\- ]/g, "")
  //         .replace(/\s+/g, "_");

  //       a.download = `${cleanTitle}.mp4`;

  //       document.body.appendChild(a);
  //       a.click();
  //       document.body.removeChild(a);

  //       window.URL.revokeObjectURL(url);
  //     })
  //     .catch((err) => {
  //       console.error("Download failed", err);
  //       alert("Tải video thất bại. Kiểm tra lại link.");
  //     })
  //     .finally(() => {
  //       setIsDownloading(false);
  //     });
  // }

  const shareLabel = {
    YouTube: "Chia sẻ lên YouTube",
    TikTok: "Chia sẻ lên TikTok",
    Facebook: "Chia sẻ lên Facebook",
  };

  const shareButtonColor = {
    YouTube: "bg-red-600 hover:bg-red-700 text-white",
    TikTok: "bg-black hover:bg-gray-800 text-white",
    Facebook: "bg-blue-600 hover:bg-blue-700 text-white",
  };

  const platformButtonClass = (name) =>
    platform === name
      ? "text-red-600 border-b-2 border-red-600 font-medium"
      : "text-gray-500 hover:text-black";

  return (
    <div
      className="fixed inset-0 z-40 bg-black/30 backdrop-blur-sm flex items-center justify-center"
      onClick={onClose}
    >
      <div
        className="bg-white w-full max-w-5xl rounded-lg shadow-2xl p-6 z-50"
        onClick={stopPropagation}
      >
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Xem trước video</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-black text-2xl font-bold"
          >
            &times;
          </button>
        </div>

        {/* Body */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Video */}
          <div className="flex items-center justify-center border rounded-md h-64 bg-black overflow-hidden">
            {loadingVideo ? (
              <div className="animate-spin h-10 w-10 border-4 border-white border-t-transparent rounded-full"></div>
            ) : (
              <video
                width="100%"
                height="400"
                controls
                preload="metadata"
                className="w-full aspect-video rounded-lg"
                poster="/placeholder.svg?height=400&width=600"
            >
                <source src={mockVideo.videoURL || mockVideo.videoID} type="video/mp4" />
                <source src={mockVideo.videoURL || mockVideo.videoID} type="video/webm" />
                <source src={mockVideo.videoURL || mockVideo.videoID} type="video/ogg" />
                Trình duyệt của bạn không hỗ trợ thẻ video.
            </video>
            )}
          </div>

          {/* Form */}
          <div>
            <div className="flex space-x-6 mb-4">
              {["YouTube", "TikTok", "Facebook"].map((name) => (
                <button
                  key={name}
                  onClick={() => setPlatform(name)}
                  className={platformButtonClass(name)}
                >
                  {name}
                </button>
              ))}
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium">Kênh</label>
                <div className="mt-1 p-2 bg-gray-100 rounded">
                  {loadingVideo ? "..." : videoData.user}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Tiêu đề video</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Nhập tiêu đề..."
                  className="w-full p-2 border rounded"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Mô tả</label>
                <textarea
                  rows="3"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Nhập mô tả..."
                  className="w-full p-2 border rounded"
                />
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                className={`flex-1 py-2 rounded font-medium ${shareButtonColor[platform]}`}
              >
                {shareLabel[platform]}
              </button>
              <button
                //onClick={handleDownload}
                disabled={isDownloading}
                className={`flex-1 py-2 rounded font-medium flex items-center justify-center ${
                  isDownloading
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                }`}
              >
                {isDownloading ? (
                  <>
                    <svg
                      className="animate-spin h-4 w-4 mr-2 text-gray-600"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                      />
                    </svg>
                    Đang tải...
                  </>
                ) : (
                  "Lưu video"
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-between items-center">
          <div className="text-sm text-gray-500">
            Tạo nội dung cho các nền tảng
          </div>
          <button
            //onClick={handleAutoCaption}
            className="px-4 py-2 bg-gray-200 text-sm rounded hover:bg-gray-300"
          >
            Tạo caption tự động
          </button>
        </div>
      </div>
    </div>
  );
}

export default Review;

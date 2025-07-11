"use client";
import { useState, useEffect, useRef } from "react";

function Review({ onClose, exportData, onConfirmUpload }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const descriptionRef = useRef(null);

  useEffect(() => {
    if (exportData) {
      const clipCount = exportData.clips ? exportData.clips.length : 0;
      const duration = exportData.timeline
        ? exportData.timeline.totalDuration
        : 0;
      const autoTitle = `Edited video - ${clipCount} clips (${Math.floor(
        duration / 60
      )}:${Math.floor(duration % 60)
        .toString()
        .padStart(2, "0")})`;
      setTitle(autoTitle);

      const autoDescription = `This video was created from ${clipCount} clips with a total duration of ${Math.floor(
        duration / 60
      )} minutes and ${Math.floor(duration % 60)} seconds.`;
      setDescription(autoDescription);
    }
  }, [exportData]);

  useEffect(() => {
    if (descriptionRef.current) {
      descriptionRef.current.style.height = "auto";
      descriptionRef.current.style.height =
        descriptionRef.current.scrollHeight + "px";
    }
  }, [description]);

  const stopPropagation = (e) => e.stopPropagation();

  function handleAutoCaption() {
    if (!exportData) return;
    const clipInfo = exportData.clips
      ? exportData.clips
          .map((clip, index) => {
            const duration = clip.end - clip.start;
            return `Clip ${index + 1}: ${Math.round(duration)}s`;
          })
          .join(", ")
      : "";

    const totalDuration = exportData.timeline
      ? exportData.timeline.totalDuration
      : 0;
    const autoCaption = `🎬 Professionally edited video
📊 ${clipInfo}
⏱️ Total duration: ${Math.floor(totalDuration / 60)}:${Math.round(
      totalDuration % 60
    )
      .toString()
      .padStart(2, "0")}
✨ Created with Video Editor`;
    setDescription(autoCaption);
  }

  const handleUploadToYoutube = () => {
    if (onConfirmUpload) {
      onConfirmUpload({
        title,
        description,
        exportData, // Pass the real export data
      });
      onClose(); // Đóng Review modal sau khi xác nhận upload
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div
      className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm flex items-center justify-center text-white"
      onClick={onClose}
    >
      <div
        className="bg-zinc-900 w-full max-w-4xl rounded-lg shadow-2xl p-6 z-50 max-h-[90vh] overflow-y-auto border border-zinc-700"
        onClick={stopPropagation}
      >
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Export Video to YouTube</h2>
          <button
            onClick={onClose}
            className="text-zinc-400 hover:text-white text-2xl font-bold"
          >
            &times;
          </button>
        </div>

        {/* Export Summary */}
        {exportData && (
          <div className="mb-6 p-4 bg-zinc-800 rounded-lg">
            <h3 className="font-semibold mb-3 text-white">Video Summary:</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-zinc-300">
              <div>
                <span className="text-zinc-500">Clips:</span>
                <div className="font-medium text-blue-400">
                  {exportData.clips ? exportData.clips.length : 0} clips
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Duration:</span>
                <div className="font-medium text-blue-400">
                  {formatTime(
                    exportData.timeline ? exportData.timeline.totalDuration : 0
                  )}
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Original Video:</span>
                <div className="font-medium text-blue-400 truncate">
                  {exportData.originalVideoUrl}
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Status:</span>
                <div className="font-medium text-green-400">
                  Ready to upload
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Body */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left - Video Details */}
          <div className="space-y-4">
            {exportData?.clips && exportData.clips.length > 0 && (
              <div className="bg-zinc-800 p-3 rounded-lg">
                <h4 className="font-medium mb-2">
                  Clips ({exportData.clips.length})
                </h4>
                <div className="space-y-1 max-h-32 overflow-y-auto text-sm text-zinc-300">
                  {exportData.clips.map((clip, index) => (
                    <div
                      key={clip.id || index}
                      className="flex justify-between"
                    >
                      <span>Clip {index + 1}</span>
                      <span className="text-zinc-500">
                        {formatTime(clip.start)} - {formatTime(clip.end)} (
                        {formatTime(clip.end - clip.start)})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="bg-zinc-800 p-4 rounded-lg">
              <h4 className="font-medium mb-3">Video Preview</h4>
              {exportData?.originalVideoUrl && (
                <video
                  src={exportData.originalVideoUrl}
                  controls
                  className="w-full max-h-48 rounded bg-black"
                >
                  Your browser does not support video playback.
                </video>
              )}
            </div>
          </div>

          {/* Right - Form */}
          <div>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-zinc-400">
                  YouTube Channel
                </label>
                <div className="mt-1 p-2 bg-zinc-800 rounded text-white">
                  Video Editor User
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-zinc-400">
                  Video Title *
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter video title..."
                  className="w-full p-2 bg-zinc-800 text-white border border-zinc-600 rounded focus:border-blue-500 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium text-zinc-400">
                  Description *
                </label>
                <textarea
                  ref={descriptionRef}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Enter video description..."
                  className="w-full p-2 bg-zinc-800 text-white border border-zinc-600 rounded resize-none overflow-hidden focus:border-blue-500 focus:outline-none"
                  required
                />
              </div>
            </div>
            <div className="mt-6 flex gap-3">
              <button
                onClick={handleUploadToYoutube}
                disabled={!title.trim() || !description.trim()}
                className="flex-1 py-2 rounded font-medium flex items-center justify-center text-white bg-red-600 hover:bg-red-700 disabled:bg-zinc-600 disabled:cursor-not-allowed transition-colors"
              >
                Upload to YouTube
              </button>
              <button
                onClick={() => {
                  console.log("Export data:", exportData);
                  alert("Export data has been logged to the console.");
                }}
                className="flex-1 py-2 rounded font-medium flex items-center justify-center bg-zinc-800 border border-zinc-600 text-white hover:bg-zinc-700 transition-colors"
              >
                View Data
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-between items-center">
          <div className="text-sm text-zinc-500">
            Video is ready for YouTube upload
          </div>
          <button
            onClick={handleAutoCaption}
            disabled={!exportData}
            className="px-4 py-2 bg-zinc-800 border border-zinc-600 text-sm rounded hover:bg-zinc-700 text-white disabled:opacity-50 transition-colors"
          >
            Generate Auto Description
          </button>
        </div>
      </div>
    </div>
  );
}

export default Review;

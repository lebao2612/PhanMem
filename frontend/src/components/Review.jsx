"use client";

import { useState, useEffect, useRef } from "react";

function Review({ onClose, exportData }) {
  const [platform, setPlatform] = useState("YouTube");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const descriptionRef = useRef(null);

  useEffect(() => {
    if (exportData) {
      const clipCount = exportData.clips.length;
      const duration = Math.round(exportData.timeline.totalDuration);
      const autoTitle = `Edited video - ${clipCount} clips (${Math.floor(
        duration / 60
      )}:${(duration % 60).toString().padStart(2, "0")})`;
      setTitle(autoTitle);

      const autoDescription = `This video was created from ${clipCount} clips with a total duration of ${Math.floor(
        duration / 60
      )} minutes and ${duration % 60} seconds.${
        exportData.stickers.length > 0
          ? ` Includes ${exportData.stickers.length} sticker(s).`
          : ""
      }`;
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
      .map((clip, index) => `Clip ${index + 1}: ${Math.round(clip.duration)}s`)
      .join(", ");

    const stickerInfo =
      exportData.stickers.length > 0
        ? ` Stickers: ${exportData.stickers.map((s) => s.emoji).join("")}`
        : "";

    const autoCaption = `🎬 Professionally edited video
📊 ${clipInfo}${stickerInfo}
⏱️ Total duration: ${Math.floor(
      exportData.timeline.totalDuration / 60
    )}:${Math.round(exportData.timeline.totalDuration % 60)
      .toString()
      .padStart(2, "0")}
✨ Created with Video Editor`;

    setDescription(autoCaption);
  }

  const shareLabel = {
    YouTube: "Export for YouTube",
    TikTok: "Export for TikTok",
    Facebook: "Export for Facebook",
  };

  const shareButtonColor = {
    YouTube: "bg-red-600 hover:bg-red-700",
    TikTok: "bg-black hover:bg-gray-900",
    Facebook: "bg-blue-600 hover:bg-blue-700",
  };

  const platformButtonClass = (name) =>
    platform === name
      ? "text-blue-400 border-b-2 border-blue-400 font-medium"
      : "text-zinc-400 hover:text-white";

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
          <h2 className="text-xl font-semibold">Export Video Info</h2>
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
                  {exportData.clips.length} clips
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Duration:</span>
                <div className="font-medium text-blue-400">
                  {formatTime(exportData.timeline.totalDuration)}
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Stickers:</span>
                <div className="font-medium text-blue-400">
                  {exportData.stickers.length} sticker(s)
                </div>
              </div>
              <div>
                <span className="text-zinc-500">Status:</span>
                <div className="font-medium text-green-400">
                  Ready to export
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Body */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left */}
          <div className="space-y-4">
            <div className="bg-zinc-800 p-4 rounded-lg">
              <h4 className="font-medium mb-3">Original Video</h4>
              <div className="space-y-2 text-sm text-zinc-400">
                <div className="flex justify-between">
                  <span>URL:</span>
                  <span className="text-blue-400 truncate max-w-48">
                    {exportData?.originalVideoUrl}
                  </span>
                </div>
              </div>
            </div>

            {exportData?.clips.length > 0 && (
              <div className="bg-zinc-800 p-3 rounded-lg">
                <h4 className="font-medium mb-2">Clips</h4>
                <div className="space-y-1 max-h-32 overflow-y-auto text-sm text-zinc-300">
                  {exportData.clips.map((clip, index) => (
                    <div key={clip.id} className="flex justify-between">
                      <span>Clip {index + 1}</span>
                      <span className="text-zinc-500">
                        {formatTime(clip.startTime)} -{" "}
                        {formatTime(clip.endTime)} ({formatTime(clip.duration)})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {exportData?.stickers.length > 0 && (
              <div className="bg-zinc-800 p-3 rounded-lg">
                <h4 className="font-medium mb-2">Stickers</h4>
                <div className="flex flex-wrap gap-2">
                  {exportData.stickers.map((sticker) => (
                    <div
                      key={sticker.id}
                      className="flex items-center gap-1 bg-zinc-900 px-2 py-1 rounded text-sm border-l-2 border-blue-500 text-zinc-300"
                    >
                      <span className="text-lg">{sticker.emoji}</span>
                      <span className="text-zinc-500">
                        {formatTime(sticker.startTime)} -{" "}
                        {formatTime(sticker.endTime)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right - Form */}
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
                <label className="text-sm font-medium text-zinc-400">
                  Channel
                </label>
                <div className="mt-1 p-2 bg-zinc-800 rounded text-white">
                  Video Editor User
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-zinc-400">
                  Video Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter title..."
                  className="w-full p-2 bg-zinc-800 text-white border border-zinc-600 rounded"
                />
              </div>

              <div>
                <label className="text-sm font-medium text-zinc-400">
                  Description
                </label>
                <textarea
                  ref={descriptionRef}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Enter description..."
                  className="w-full p-2 bg-zinc-800 text-white border border-zinc-600 rounded resize-none overflow-hidden"
                />
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={() => {
                  console.log("Export data:", {
                    platform,
                    title,
                    description,
                    exportData,
                  });
                  alert(
                    `Exporting to ${platform}:\n\nTitle: ${title}\n\nDescription: ${description}`
                  );
                }}
                className={`flex-1 py-2 rounded font-medium flex items-center justify-center text-white ${shareButtonColor[platform]}`}
              >
                {shareLabel[platform]}
              </button>

              <button
                onClick={() => {
                  console.log("Export data logged to console");
                  alert("Export data has been logged to the console.");
                }}
                className="flex-1 py-2 rounded font-medium flex items-center justify-center bg-zinc-800 border border-zinc-600 text-white hover:bg-zinc-700"
              >
                View Info
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-between items-center">
          <div className="text-sm text-zinc-500">
            Edited video is ready for export
          </div>
          <button
            onClick={handleAutoCaption}
            disabled={!exportData}
            className="px-4 py-2 bg-zinc-800 border border-zinc-600 text-sm rounded hover:bg-zinc-700 text-white disabled:opacity-50"
          >
            Generate Auto Desciption
          </button>
        </div>
      </div>
    </div>
  );
}

export default Review;

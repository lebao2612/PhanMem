"use client";
import { useEffect, useRef, useState, useCallback } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import Review from "../components/Review";
import UploadVideo from "../components/UploadVideo";
import {
  formatTime,
  updateEffectiveTimeline,
  handleSplitVideo,
  handleDeleteClip,
  handleUndo,
  togglePlay,
  handleTimelineClick,
  processVideoForExport,
} from "../scripts/editVideo";
import { Lock, Eye, Volume2, MoreHorizontal, Play, Pause } from "lucide-react";

const EditVideo = () => {
  const location = useLocation();
  const videoUrl = location.state?.videoUrl || "/placeholder-video.mp4"; // Default video URL for testing
  const initialGeneratedScripts = location.state?.generatedScripts || [];
  const initialGeneratedImages = location.state?.generatedImages || [];

  const videoRef = useRef(null);
  const timelineRef = useRef(null);
  const videoContainerRef = useRef(null); // Ref for the video display area

  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [dragging, setDragging] = useState(null);
  const [clips, setClips] = useState([]);
  const [selectedClipIndex, setSelectedClipIndex] = useState(null);
  const [history, setHistory] = useState([]);
  const [selectionRange, setSelectionRange] = useState(null);
  const [zoom, setZoom] = useState(1);
  const [effectiveTimeline, setEffectiveTimeline] = useState({
    duration: 0,
    segments: [],
  });
  const [rightPanelTab, setRightPanelTab] = useState("details");

  // State for Review and Upload modals
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [exportData, setExportData] = useState(null);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [uploadVideoData, setUploadVideoData] = useState(null);

  // State for text insertion and overlays
  const [textToInsert, setTextToInsert] = useState("");
  const [textOverlays, setTextOverlays] = useState([]); // Array to store text objects
  const [draggingTextId, setDraggingTextId] = useState(null); // ID of the text being dragged
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 }); // Offset for dragging

  // Mock authFetch function (replace with your actual AuthContext.authFetch)
  const authFetch = async (url, options) => {
    console.log("Mock API call from EditVideo:", url, options);
    await new Promise((resolve) => setTimeout(resolve, 2000));
    return {
      ok: true,
      json: async () => ({ success: true }),
    };
  };

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadedMetadata = () => {
      setDuration(video.duration);
      const initialClip = { id: "clip-0", start: 0, end: video.duration };
      setClips([initialClip]);
      setEffectiveTimeline({
        duration: video.duration,
        segments: [
          {
            start: 0,
            end: video.duration,
            originalStart: 0,
            originalEnd: video.duration,
          },
        ],
      });
    };

    const handleTimeUpdate = () => {
      const newVideoCurrentTime = video.currentTime;
      let effectiveTime = 0;
      if (
        clips.length > 0 &&
        newVideoCurrentTime >= clips[clips.length - 1].end
      ) {
        video.pause();
        setIsPlaying(false);
      }
      let accumulatedEffectiveDuration = 0;
      for (const segment of effectiveTimeline.segments) {
        const segmentEffectiveDuration = segment.end - segment.start;
        if (
          newVideoCurrentTime >= segment.originalStart &&
          newVideoCurrentTime < segment.originalEnd
        ) {
          effectiveTime =
            accumulatedEffectiveDuration +
            (newVideoCurrentTime - segment.originalStart);
          break;
        }
        accumulatedEffectiveDuration += segmentEffectiveDuration;
      }
      setCurrentTime(effectiveTime);
    };

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => {
      setIsPlaying(false);
    };
    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(effectiveTimeline.duration);
    };

    video.addEventListener("loadedmetadata", handleLoadedMetadata);
    video.addEventListener("timeupdate", handleTimeUpdate);
    video.addEventListener("play", handlePlay);
    video.addEventListener("pause", handlePause);
    video.addEventListener("ended", handleEnded);

    return () => {
      video.removeEventListener("loadedmetadata", handleLoadedMetadata);
      video.removeEventListener("timeupdate", handleTimeUpdate);
      video.removeEventListener("play", handlePlay);
      video.removeEventListener("pause", handlePause);
      video.removeEventListener("ended", handleEnded);
    };
  }, [clips, effectiveTimeline]);

  useEffect(() => {
    updateEffectiveTimeline(clips, setEffectiveTimeline);
  }, [clips]);

  // --- Dragging for timeline elements (existing logic) ---
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!dragging || !timelineRef.current || !effectiveTimeline.duration)
        return;
      const rect = timelineRef.current.getBoundingClientRect();
      const pos = Math.min(Math.max(e.clientX - rect.left, 0), rect.width);
      const time = (pos / rect.width) * effectiveTimeline.duration;
      if (dragging.type === "playhead") {
        let originalVideoTime = 0;
        let accumulatedEffectiveDuration = 0;
        for (const segment of effectiveTimeline.segments) {
          const segmentEffectiveDuration = segment.end - segment.start;
          if (
            time >= accumulatedEffectiveDuration &&
            time < accumulatedEffectiveDuration + segmentEffectiveDuration
          ) {
            originalVideoTime =
              segment.originalStart + (time - accumulatedEffectiveDuration);
            break;
          }
          accumulatedEffectiveDuration += segmentEffectiveDuration;
        }
        setCurrentTime(time);
        videoRef.current.currentTime = originalVideoTime;
      } else if (dragging.type === "clip-start") {
        setClips((prev) =>
          prev.map((clip, index) =>
            index === dragging.clipIndex
              ? { ...clip, start: Math.min(time, clip.end - 0.1) }
              : clip
          )
        );
      } else if (dragging.type === "clip-end") {
        setClips((prev) =>
          prev.map((clip, index) =>
            index === dragging.clipIndex
              ? { ...clip, end: Math.max(time, clip.start + 0.1) }
              : clip
          )
        );
      }
    };

    const handleMouseUp = () => {
      setDragging(null);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragging, effectiveTimeline.duration, effectiveTimeline.segments]);

  // Function to open UploadVideo modal from Review
  const handleConfirmUploadFromReview = (data) => {
    setUploadVideoData({
      id: `video_${Date.now()}`, // Generate or use a real video ID
      title: data.title,
      description: data.description,
      createdAt: new Date().toISOString(),
      exportData: data.exportData, // Pass the full export data
    });
    setIsReviewOpen(false); // Close Review modal
    setIsUploadOpen(true); // Open UploadVideo modal
  };

  // --- New Text Insertion Logic ---
  const handleInsertText = () => {
    if (textToInsert.trim()) {
      const newTextOverlay = {
        id: `text-${Date.now()}`,
        text: textToInsert,
        x: 50, // Initial X position (percentage from left)
        y: 50, // Initial Y position (percentage from top)
        startTime: currentTime,
        endTime: currentTime + 5, // Display for 5 seconds by default
      };
      setTextOverlays((prev) => [...prev, newTextOverlay]);
      setTextToInsert(""); // Clear the input after insertion
      console.log("Text inserted:", newTextOverlay);
    } else {
      alert("Please enter some text to insert.");
    }
  };

  // --- Drag and Drop for Text Overlays ---
  const handleTextMouseDown = useCallback((e, id) => {
    e.stopPropagation(); // Prevent dragging the video playhead
    setDraggingTextId(id);
    const textElement = e.target;
    const rect = textElement.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  }, []);

  const handleVideoContainerMouseMove = useCallback(
    (e) => {
      if (!draggingTextId || !videoContainerRef.current) return;

      const videoRect = videoContainerRef.current.getBoundingClientRect();
      const newX = e.clientX - videoRect.left - dragOffset.x;
      const newY = e.clientY - videoRect.top - dragOffset.y;

      // Convert pixel coordinates to percentages relative to video container
      const newXPercent = (newX / videoRect.width) * 100;
      const newYPercent = (newY / videoRect.height) * 100;

      setTextOverlays((prev) =>
        prev.map((overlay) =>
          overlay.id === draggingTextId
            ? {
                ...overlay,
                x: Math.max(0, Math.min(100, newXPercent)), // Clamp between 0 and 100
                y: Math.max(0, Math.min(100, newYPercent)), // Clamp between 0 and 100
              }
            : overlay
        )
      );
    },
    [draggingTextId, dragOffset]
  );

  const handleVideoContainerMouseUp = useCallback(() => {
    setDraggingTextId(null);
    setDragOffset({ x: 0, y: 0 });
  }, []);

  return (
    <div className="relative flex h-screen bg-[#1a1a1a] text-white overflow-hidden">
      <LeftSideBar />
      <div className="flex-1 flex flex-col">
        <Header />
        <div className="flex-1 flex overflow-hidden">
          <div className="flex-1 flex flex-col bg-[#1a1a1a]">
            <div className="flex-1 flex items-center justify-center bg-[#0f0f0f] border-b border-gray-700 relative">
              {videoUrl ? (
                <div
                  ref={videoContainerRef}
                  className="relative w-full h-full flex items-center justify-center" // Ensure container fills space
                  onMouseMove={handleVideoContainerMouseMove}
                  onMouseUp={handleVideoContainerMouseUp}
                  onMouseLeave={handleVideoContainerMouseUp} // Stop dragging if mouse leaves container
                >
                  <video
                    ref={videoRef}
                    src={videoUrl}
                    className="max-h-[60vh] max-w-full rounded-lg shadow-2xl"
                    controls={false}
                    onClick={() =>
                      togglePlay(videoRef.current, isPlaying, setIsPlaying)
                    }
                  />
                  {/* Render text overlays */}
                  {textOverlays
                    .filter(
                      (overlay) =>
                        currentTime >= overlay.startTime &&
                        currentTime <= overlay.endTime
                    )
                    .map((overlay) => (
                      <div
                        key={overlay.id}
                        className="absolute text-white text-4xl font-bold pointer-events-auto cursor-grab active:cursor-grabbing select-none"
                        style={{
                          left: `${overlay.x}%`,
                          top: `${overlay.y}%`,
                          transform: "translate(-50%, -50%)", // Center the text element
                          textShadow: "2px 2px 4px rgba(0,0,0,0.7)",
                          zIndex: 10, // Ensure text is above video
                        }}
                        onMouseDown={(e) => handleTextMouseDown(e, overlay.id)}
                      >
                        {overlay.text}
                      </div>
                    ))}

                  <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center gap-4 bg-black/70 px-4 py-2 rounded-lg">
                    <button
                      onClick={() =>
                        togglePlay(videoRef.current, isPlaying, setIsPlaying)
                      }
                      className="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all"
                    >
                      {isPlaying ? (
                        <Pause className="w-5 h-5" />
                      ) : (
                        <Play className="w-5 h-5 ml-1" />
                      )}
                    </button>
                    <div className="text-sm font-mono">
                      <span className="text-cyan-400">
                        {formatTime(currentTime * 1000)}
                      </span>
                      <span className="text-gray-400 mx-2">/</span>
                      <span className="text-gray-300">
                        {formatTime(effectiveTimeline.duration * 1000)}
                      </span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center">
                  <div className="text-6xl mb-4">🎬</div>
                  <p className="text-gray-400 text-lg">No video loaded</p>
                </div>
              )}
            </div>
            <div className="h-64 bg-[#1a1a1a] border-t border-gray-700 flex flex-col">
              <div className="flex items-center justify-between px-4 py-2 bg-[#2a2a2a] border-b border-gray-600">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() =>
                      handleSplitVideo(
                        currentTime,
                        effectiveTimeline,
                        clips,
                        setClips,
                        setHistory,
                        setSelectedClipIndex
                      )
                    }
                    className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-700 rounded text-sm font-medium transition-colors"
                  >
                    Split
                  </button>
                  <button
                    onClick={() =>
                      handleDeleteClip(
                        selectedClipIndex,
                        clips,
                        setClips,
                        setHistory,
                        setSelectedClipIndex
                      )
                    }
                    className="px-3 py-1.5 bg-red-600 hover:bg-red-700 rounded text-sm font-medium transition-colors disabled:opacity-50"
                    disabled={selectedClipIndex === null}
                  >
                    Delete
                  </button>
                  <button
                    onClick={() =>
                      handleUndo(
                        history,
                        setClips,
                        setHistory,
                        setSelectedClipIndex,
                        setSelectionRange
                      )
                    }
                    className="px-3 py-1.5 bg-gray-600 hover:bg-gray-700 rounded text-sm font-medium transition-colors disabled:opacity-50"
                    disabled={history.length === 0}
                  >
                    Undo
                  </button>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-sm text-gray-400">
                    {selectionRange && (
                      <span className="text-yellow-400 mr-4">
                        Selection:{" "}
                        {formatTime(
                          (selectionRange.end - selectionRange.start) * 1000
                        )}
                      </span>
                    )}
                    Zoom: {Math.round(zoom * 100)}%
                  </div>
                  <input
                    type="range"
                    min="0.5"
                    max="3"
                    step="0.1"
                    value={zoom}
                    onChange={(e) => setZoom(Number.parseFloat(e.target.value))}
                    className="w-20"
                  />
                  <button
                    onClick={() => {
                      const exportData = processVideoForExport(
                        videoUrl,
                        clips,
                        effectiveTimeline
                      );
                      setIsReviewOpen(true);
                      setExportData(exportData);
                    }}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium transition-colors flex items-center gap-2"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
                      />
                    </svg>
                    Export
                  </button>
                </div>
              </div>
              <div className="flex-1 flex">
                {/* Left Track Controls */}
                <div className="w-20 bg-[#2a2a2a] border-r border-gray-600 flex flex-col">
                  <div className="h-12 flex items-center justify-center border-b border-gray-600 text-xs font-medium">
                    Video
                  </div>
                  <div className="flex-1 flex flex-col justify-around items-center py-2">
                    <div className="flex flex-col items-center gap-2">
                      <Lock className="w-4 h-4 text-gray-500" />
                      <Eye className="w-4 h-4 text-gray-500" />
                      <Volume2 className="w-4 h-4 text-gray-500" />
                      <MoreHorizontal className="w-4 h-4 text-gray-500" />
                    </div>
                  </div>
                </div>
                <div className="flex-1 relative overflow-x-auto">
                  <div className="h-8 bg-[#2a2a2a] border-b border-gray-600 relative">
                    {Array.from(
                      {
                        length: Math.ceil(effectiveTimeline.duration / 10) + 1,
                      },
                      (_, i) => (
                        <div
                          key={i}
                          className="absolute top-0 h-full flex flex-col justify-center"
                          style={{
                            left: `${
                              ((i * 10) / effectiveTimeline.duration) *
                              100 *
                              zoom
                            }%`,
                          }}
                        >
                          <div className="w-px h-2 bg-gray-500"></div>
                          <div className="text-xs text-gray-400 ml-1">
                            {formatTime(i * 10 * 1000)}
                          </div>
                        </div>
                      )
                    )}
                  </div>
                  {/* Playhead moved here, spanning both video and audio tracks */}
                  <div
                    className="absolute top-8 w-0.5 h-16 bg-white cursor-ew-resize z-30 shadow-lg" /* h-16 (video) */
                    style={{
                      left: `${
                        (currentTime / effectiveTimeline.duration) * 100
                      }%`,
                    }}
                    onMouseDown={() => setDragging({ type: "playhead" })}
                  >
                    <div className="absolute -top-2 -left-3 w-6 h-4 bg-white clip-path-triangle"></div>
                    <div className="absolute -bottom-2 -left-3 w-6 h-4 bg-white clip-path-triangle rotate-180"></div>
                  </div>
                  <div
                    ref={timelineRef}
                    className="h-16 bg-[#1a1a1a] border-b border-gray-600 relative cursor-pointer"
                    onClick={(e) =>
                      handleTimelineClick(
                        e,
                        timelineRef,
                        effectiveTimeline,
                        effectiveTimeline.duration,
                        currentTime,
                        setCurrentTime,
                        setSelectionRange,
                        videoRef,
                        clips,
                        setSelectedClipIndex
                      )
                    }
                    style={{
                      width: `${
                        (effectiveTimeline.duration / duration) * 100 * zoom
                      }%`,
                    }}
                  >
                    {selectionRange && (
                      <div
                        className="absolute top-0 h-full bg-yellow-500/30 border-2 border-yellow-500"
                        style={{
                          left: `${
                            (selectionRange.start /
                              effectiveTimeline.duration) *
                            100
                          }%`,
                          width: `${
                            ((selectionRange.end - selectionRange.start) /
                              effectiveTimeline.duration) *
                            100
                          }%`,
                        }}
                      />
                    )}
                    {effectiveTimeline.segments.map((segment, index) => {
                      const clip = clips[index];
                      if (!clip) return null;
                      return (
                        <div
                          key={clip.id || index}
                          className="absolute top-1 h-14"
                          style={{
                            left: `${
                              (segment.start / effectiveTimeline.duration) * 100
                            }%`,
                            width: `${
                              ((segment.end - segment.start) /
                                effectiveTimeline.duration) *
                              100
                            }%`,
                            minWidth: "40px",
                          }}
                        >
                          <div
                            className={`h-full rounded border-2 transition-all relative overflow-hidden ${
                              selectedClipIndex === index
                                ? "border-cyan-400 bg-cyan-600/80"
                                : "border-cyan-500/50 bg-cyan-600/60"
                            }`}
                          >
                            <div className="p-1 text-xs font-medium text-white truncate">
                              {clip.id || `Clip ${index + 1}`}
                            </div>
                            <div className="absolute bottom-1 left-1 text-xs text-cyan-100 font-mono">
                              {formatTime((clip.end - clip.start) * 1000)}
                            </div>
                            <div
                              className="absolute left-0 top-0 w-2 h-full bg-cyan-300 cursor-ew-resize opacity-0 hover:opacity-100 transition-opacity"
                              onMouseDown={(e) => {
                                e.stopPropagation();
                                setDragging({
                                  type: "clip-start",
                                  clipIndex: index,
                                });
                              }}
                            />
                            <div
                              className="absolute right-0 top-0 w-2 h-full bg-cyan-300 cursor-ew-resize opacity-0 hover:opacity-100 transition-opacity"
                              onMouseDown={(e) => {
                                e.stopPropagation();
                                setDragging({
                                  type: "clip-end",
                                  clipIndex: index,
                                });
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="w-80 bg-[#2a2a2a] border-l border-gray-600 flex flex-col">
            <div className="flex border-b border-gray-600">
              <button
                onClick={() => setRightPanelTab("details")}
                className={`flex-1 p-3 text-sm font-medium transition-colors ${
                  rightPanelTab === "details"
                    ? "bg-cyan-600 text-white"
                    : "text-gray-400 hover:text-white hover:bg-gray-700"
                }`}
              >
                Details
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {rightPanelTab === "details" && (
                <div className="space-y-4">
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">
                      Video Properties
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Duration:</span>
                        <span>{formatTime(duration * 1000)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Current Time:</span>
                        <span className="text-cyan-400">
                          {formatTime(currentTime * 1000)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Clips:</span>
                        <span>{clips.length}</span>
                      </div>
                    </div>
                  </div>
                  {clips.length > 0 && (
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-300">Clips</h4>
                      <div className="space-y-2">
                        {clips.map((clip, index) => (
                          <div
                            key={clip.id || index}
                            className={`p-3 rounded border cursor-pointer transition-all ${
                              selectedClipIndex === index
                                ? "border-cyan-400 bg-cyan-900/20"
                                : "border-gray-600 bg-gray-700/30 hover:bg-gray-700/50"
                            }`}
                            onClick={() => setSelectedClipIndex(index)}
                          >
                            <div className="flex justify-between items-center mb-1">
                              <span className="font-medium text-sm">
                                {clip.id || `Clip ${index + 1}`}
                              </span>
                              <span className="text-xs text-gray-400">
                                {formatTime((clip.end - clip.start) * 1000)}
                              </span>
                            </div>
                            <div className="text-xs text-gray-500">
                              {formatTime(clip.start * 1000)} →{" "}
                              {formatTime(clip.end * 1000)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Text Insertion Section */}
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">Insert Text</h4>
                    <textarea
                      placeholder="Enter text to insert..."
                      value={textToInsert}
                      onChange={(e) => setTextToInsert(e.target.value)}
                      rows={3}
                      className="w-full p-2 bg-zinc-800 text-white border border-zinc-600 rounded resize-none focus:border-blue-500 focus:outline-none text-sm"
                    />
                    <button
                      onClick={handleInsertText}
                      disabled={!textToInsert.trim()}
                      className="w-full py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Insert Text
                    </button>
                  </div>

                  {/* Display current text overlays (for debugging/management) */}
                  {textOverlays.length > 0 && (
                    <div className="space-y-3 mt-6">
                      <h4 className="font-medium text-gray-300">
                        Active Text Overlays
                      </h4>
                      <div className="space-y-2 text-sm text-zinc-300">
                        {textOverlays.map((overlay) => (
                          <div
                            key={overlay.id}
                            className="p-2 bg-zinc-800 rounded border border-zinc-700"
                          >
                            <p className="truncate">"{overlay.text}"</p>
                            <p className="text-xs text-zinc-500">
                              Time: {formatTime(overlay.startTime * 1000)} -{" "}
                              {formatTime(overlay.endTime * 1000)}
                            </p>
                            <p className="text-xs text-zinc-500">
                              Pos: {overlay.x.toFixed(1)}%,{" "}
                              {overlay.y.toFixed(1)}%
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      {isReviewOpen && (
        <Review
          onClose={() => {
            setIsReviewOpen(false);
            setExportData(null);
          }}
          exportData={exportData}
          onConfirmUpload={handleConfirmUploadFromReview} // Pass the new handler
        />
      )}
      {isUploadOpen &&
        uploadVideoData && ( // Render UploadVideo as a top-level modal
          <UploadVideo
            selectedVideo={uploadVideoData}
            onClose={() => {
              setIsUploadOpen(false);
              setUploadVideoData(null);
            }}
            onBack={() => {
              setIsUploadOpen(false);
              setIsReviewOpen(true); // Go back to Review modal
            }}
            authFetch={authFetch} // Pass authFetch
          />
        )}
      <style>{`
        .clip-path-triangle {
          clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        }
      `}</style>
    </div>
  );
};

export default EditVideo;

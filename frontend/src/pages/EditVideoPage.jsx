"use client";

import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import Review from "../components/Review";
import {
  formatTime,
  updateEffectiveTimeline,
  addSticker,
  deleteSticker,
  handleSplitVideo,
  handleDeleteSelection,
  handleDeleteClip,
  handleUndo,
  togglePlay,
  handleTimelineClick,
  processVideoForExport,
} from "../scripts/editVideo";

const EditVideo = () => {
  const location = useLocation();
  const videoUrl = location.state?.videoUrl;
  const videoRef = useRef(null);
  const timelineRef = useRef(null);
  const videoContainerRef = useRef(null);

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

  // Sticker states
  const [stickers, setStickers] = useState([]);
  const [selectedSticker, setSelectedSticker] = useState(null);
  const [stickerDragging, setStickerDragging] = useState(null);
  const [rightPanelTab, setRightPanelTab] = useState("details"); // 'details' or 'stickers'

  // Export states
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [exportData, setExportData] = useState(null);

  // Available stickers
  const availableStickers = [
    { id: "heart", emoji: "❤️", name: "Heart" },
    { id: "star", emoji: "⭐", name: "Star" },
    { id: "fire", emoji: "🔥", name: "Fire" },
    { id: "thumbs-up", emoji: "👍", name: "Thumbs Up" },
    { id: "smile", emoji: "😊", name: "Smile" },
    { id: "laugh", emoji: "😂", name: "Laugh" },
    { id: "cool", emoji: "😎", name: "Cool" },
    { id: "party", emoji: "🎉", name: "Party" },
    { id: "rocket", emoji: "🚀", name: "Rocket" },
    { id: "diamond", emoji: "💎", name: "Diamond" },
    { id: "crown", emoji: "👑", name: "Crown" },
    { id: "lightning", emoji: "⚡", name: "Lightning" },
    { id: "rainbow", emoji: "🌈", name: "Rainbow" },
    { id: "unicorn", emoji: "🦄", name: "Unicorn" },
    { id: "pizza", emoji: "🍕", name: "Pizza" },
    { id: "music", emoji: "🎵", name: "Music" },
  ];

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
      const newTime = video.currentTime;
      let effectiveTime = 0;
      let foundSegment = null;

      for (const segment of effectiveTimeline.segments) {
        const segmentDuration = segment.end - segment.start;
        if (
          newTime >= segment.originalStart &&
          newTime <= segment.originalEnd
        ) {
          effectiveTime += newTime - segment.originalStart;
          foundSegment = segment;
          break;
        } else if (newTime < segment.originalStart) {
          break;
        } else {
          effectiveTime += segmentDuration;
        }
      }

      if (!foundSegment && effectiveTimeline.segments.length > 0) {
        const nextSegment = effectiveTimeline.segments.find(
          (seg) => seg.originalStart > newTime
        );
        if (nextSegment) {
          video.currentTime = nextSegment.originalStart;
          return;
        } else {
          video.pause();
          setIsPlaying(false);
          return;
        }
      }

      setCurrentTime(effectiveTime);
    };

    video.addEventListener("loadedmetadata", handleLoadedMetadata);
    video.addEventListener("timeupdate", handleTimeUpdate);

    return () => {
      video.removeEventListener("loadedmetadata", handleLoadedMetadata);
      video.removeEventListener("timeupdate", handleTimeUpdate);
    };
  }, [effectiveTimeline]);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (stickerDragging && videoContainerRef.current) {
        const rect = videoContainerRef.current.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;

        if (x < -5 || x > 105 || y < -5 || y > 105) {
          setStickers((prev) =>
            prev.filter((sticker) => sticker.id !== stickerDragging.id)
          );
          setStickerDragging(null);
          setSelectedSticker(null);
          return;
        }

        setStickers((prev) =>
          prev.map((sticker) =>
            sticker.id === stickerDragging.id
              ? {
                  ...sticker,
                  x: Math.max(-2, Math.min(102, x)),
                  y: Math.max(-2, Math.min(102, y)),
                }
              : sticker
          )
        );
        return;
      }

      if (!dragging || !timelineRef.current || !duration) return;

      const rect = timelineRef.current.getBoundingClientRect();
      const pos = Math.min(Math.max(e.clientX - rect.left, 0), rect.width);
      const time = (pos / rect.width) * duration;

      if (dragging.type === "playhead") {
        setCurrentTime(time);
        videoRef.current.currentTime = time;
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
      setStickerDragging(null);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragging, stickerDragging, duration]);

  // Add this useEffect to update sticker timing when video duration changes
  useEffect(() => {
    if (effectiveTimeline.duration > 0) {
      setStickers((prev) =>
        prev.map((sticker) => ({
          ...sticker,
          endTime:
            sticker.endTime >= effectiveTimeline.duration - 0.1
              ? effectiveTimeline.duration
              : sticker.endTime,
        }))
      );
    }
  }, [effectiveTimeline.duration]);

  return (
    <div className="relative flex h-screen bg-[#1a1a1a] text-white overflow-hidden">
      <LeftSideBar />

      <div className="flex-1 flex flex-col">
        <Header />

        {/* Main Content Area - CapCut Style Layout */}
        <div className="flex-1 flex overflow-hidden">
          {/* Center Content */}
          <div className="flex-1 flex flex-col bg-[#1a1a1a]">
            {/* Video Preview Area */}
            <div className="flex-1 flex items-center justify-center bg-[#0f0f0f] border-b border-gray-700 relative">
              {videoUrl ? (
                <div
                  ref={videoContainerRef}
                  className={`relative ${
                    stickerDragging
                      ? "ring-2 ring-dashed ring-cyan-400 ring-opacity-50"
                      : ""
                  }`}
                  onClick={() => setSelectedSticker(null)}
                >
                  <video
                    ref={videoRef}
                    src={videoUrl}
                    className="max-h-[60vh] max-w-full rounded-lg shadow-2xl"
                    controls={false}
                    onClick={() =>
                      togglePlay(
                        videoRef.current,
                        isPlaying,
                        setIsPlaying,
                        currentTime
                      )
                    }
                  />

                  {/* Drag boundary indicator */}
                  {stickerDragging && (
                    <div className="absolute inset-0 pointer-events-none">
                      <div className="absolute inset-2 border-2 border-dashed border-cyan-400 opacity-30 rounded"></div>
                      <div className="absolute -inset-4 border-2 border-dashed border-red-400 opacity-20 rounded"></div>
                    </div>
                  )}

                  {/* Stickers Overlay */}
                  {stickers.map((sticker) => {
                    const isVisible =
                      currentTime >= sticker.startTime &&
                      currentTime <= sticker.endTime;
                    if (!isVisible) return null;

                    const isDragging = stickerDragging?.id === sticker.id;
                    const isNearBoundary =
                      sticker.x < 5 ||
                      sticker.x > 95 ||
                      sticker.y < 5 ||
                      sticker.y > 95;

                    return (
                      <div
                        key={sticker.id}
                        className={`absolute cursor-move select-none transition-all duration-150 ease-out ${
                          selectedSticker === sticker.id
                            ? "ring-2 ring-cyan-400 ring-opacity-80"
                            : ""
                        } ${isDragging ? "scale-110 z-50" : "z-10"} ${
                          isNearBoundary && isDragging
                            ? "opacity-50 scale-90"
                            : ""
                        }`}
                        style={{
                          left: `${sticker.x}%`,
                          top: `${sticker.y}%`,
                          fontSize: `${sticker.size}px`,
                          transform: `translate(-50%, -50%) rotate(${
                            sticker.rotation
                          }deg) ${isDragging ? "scale(1.1)" : "scale(1)"}`,
                          filter: isDragging
                            ? "drop-shadow(0 8px 16px rgba(0,0,0,0.3))"
                            : "none",
                          transition: isDragging ? "none" : "all 0.2s ease-out",
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedSticker(sticker.id);
                        }}
                        onMouseDown={(e) => {
                          e.stopPropagation();
                          setStickerDragging(sticker);
                          setSelectedSticker(sticker.id);
                        }}
                      >
                        {sticker.emoji}
                        {selectedSticker === sticker.id && !isDragging && (
                          <button
                            className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full text-white text-xs flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg"
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteSticker(
                                sticker.id,
                                setStickers,
                                setSelectedSticker
                              );
                            }}
                          >
                            ×
                          </button>
                        )}
                        {isDragging && isNearBoundary && (
                          <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-red-500 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                            Release to delete
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {/* Video Controls Overlay */}
                  <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center gap-4 bg-black/70 px-4 py-2 rounded-lg">
                    <button
                      onClick={() =>
                        togglePlay(
                          videoRef.current,
                          isPlaying,
                          setIsPlaying,
                          currentTime
                        )
                      }
                      className="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all"
                    >
                      {isPlaying ? (
                        <svg
                          className="w-5 h-5"
                          fill="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                        </svg>
                      ) : (
                        <svg
                          className="w-5 h-5 ml-1"
                          fill="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path d="M8 5v14l11-7z" />
                        </svg>
                      )}
                    </button>

                    <div className="text-sm font-mono">
                      <span className="text-cyan-400">
                        {formatTime(currentTime)}
                      </span>
                      <span className="text-gray-400 mx-2">/</span>
                      <span className="text-gray-300">
                        {formatTime(effectiveTimeline.duration)}
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

            {/* Timeline Area - CapCut Style */}
            <div className="h-64 bg-[#1a1a1a] border-t border-gray-700 flex flex-col">
              {/* Timeline Controls */}
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
                        setSelectedClipIndex,
                        updateEffectiveTimeline
                      )
                    }
                    className="px-3 py-1.5 bg-red-600 hover:bg-red-700 rounded text-sm font-medium transition-colors disabled:opacity-50"
                    disabled={selectedClipIndex === null}
                  >
                    Delete
                  </button>
                  <button
                    onClick={() =>
                      handleDeleteSelection(
                        selectionRange,
                        clips,
                        setClips,
                        setHistory,
                        setSelectionRange,
                        setSelectedClipIndex,
                        updateEffectiveTimeline
                      )
                    }
                    className="px-3 py-1.5 bg-orange-600 hover:bg-orange-700 rounded text-sm font-medium transition-colors disabled:opacity-50"
                    disabled={!selectionRange}
                  >
                    Delete Range
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
                        {formatTime(selectionRange.end - selectionRange.start)}
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

                  {/* Export Button */}
                  <button
                    onClick={() => {
                      const exportData = processVideoForExport(
                        videoUrl,
                        clips,
                        stickers,
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

              {/* Timeline Tracks */}
              <div className="flex-1 flex">
                {/* Track Labels */}
                <div className="w-20 bg-[#2a2a2a] border-r border-gray-600 flex flex-col">
                  <div className="h-12 flex items-center justify-center border-b border-gray-600 text-xs font-medium">
                    Video
                  </div>
                  <div className="h-12 flex items-center justify-center border-b border-gray-600 text-xs font-medium text-gray-500">
                    Audio
                  </div>
                </div>

                {/* Timeline Content */}
                <div className="flex-1 relative overflow-x-auto">
                  {/* Time Ruler */}
                  <div className="h-8 bg-[#2a2a2a] border-b border-gray-600 relative">
                    {Array.from(
                      { length: Math.ceil(duration / 10) + 1 },
                      (_, i) => (
                        <div
                          key={i}
                          className="absolute top-0 h-full flex flex-col justify-center"
                          style={{
                            left: `${((i * 10) / duration) * 100 * zoom}%`,
                          }}
                        >
                          <div className="w-px h-2 bg-gray-500"></div>
                          <div className="text-xs text-gray-400 ml-1">
                            {formatTime(i * 10)}
                          </div>
                        </div>
                      )
                    )}
                  </div>

                  {/* Video Track */}
                  <div
                    ref={timelineRef}
                    className="h-16 bg-[#1a1a1a] border-b border-gray-600 relative cursor-pointer"
                    onClick={(e) =>
                      handleTimelineClick(
                        e,
                        timelineRef,
                        effectiveTimeline,
                        duration,
                        currentTime,
                        setCurrentTime,
                        setSelectionRange,
                        videoRef,
                        clips,
                        setSelectedClipIndex
                      )
                    }
                    style={{ width: `${100 * zoom}%` }}
                  >
                    {/* Selection Range */}
                    {selectionRange && (
                      <div
                        className="absolute top-0 h-full bg-yellow-500/30 border-2 border-yellow-500"
                        style={{
                          left: `${(selectionRange.start / duration) * 100}%`,
                          width: `${
                            ((selectionRange.end - selectionRange.start) /
                              duration) *
                            100
                          }%`,
                        }}
                      />
                    )}

                    {/* Video Clips - CapCut Style */}
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
                            } hover:border-cyan-300`}
                          >
                            <div className="p-1 text-xs font-medium text-white truncate">
                              {clip.id || `Clip ${index + 1}`}
                            </div>

                            <div className="absolute bottom-1 left-1 text-xs text-cyan-100 font-mono">
                              {formatTime(clip.end - clip.start)}
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

                    {/* Playhead - CapCut Style */}
                    <div
                      className="absolute top-0 w-0.5 h-full bg-white cursor-ew-resize z-30 shadow-lg"
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
                  </div>

                  {/* Audio Track Placeholder */}
                  <div className="h-12 bg-[#1a1a1a] border-b border-gray-600 relative">
                    <div className="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">
                      Audio Track
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Sidebar - Enhanced with Stickers */}
          <div className="w-80 bg-[#2a2a2a] border-l border-gray-600 flex flex-col">
            {/* Tab Navigation */}
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
              <button
                onClick={() => setRightPanelTab("stickers")}
                className={`flex-1 p-3 text-sm font-medium transition-colors ${
                  rightPanelTab === "stickers"
                    ? "bg-cyan-600 text-white"
                    : "text-gray-400 hover:text-white hover:bg-gray-700"
                }`}
              >
                Stickers
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
              {rightPanelTab === "details" ? (
                <div className="space-y-4">
                  {/* Video Properties */}
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">
                      Video Properties
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Duration:</span>
                        <span>{formatTime(duration)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Current Time:</span>
                        <span className="text-cyan-400">
                          {formatTime(currentTime)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Clips:</span>
                        <span>{clips.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Stickers:</span>
                        <span>{stickers.length}</span>
                      </div>
                    </div>
                  </div>

                  {/* Clip List */}
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
                                {formatTime(clip.end - clip.start)}
                              </span>
                            </div>
                            <div className="text-xs text-gray-500">
                              {formatTime(clip.start)} → {formatTime(clip.end)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Selected Sticker Properties */}
                  {selectedSticker && (
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-300">
                        Selected Sticker
                      </h4>
                      <div className="space-y-3">
                        {(() => {
                          const sticker = stickers.find(
                            (s) => s.id === selectedSticker
                          );
                          if (!sticker) return null;

                          return (
                            <>
                              <div>
                                <label className="block text-sm text-gray-400 mb-1">
                                  Size
                                </label>
                                <input
                                  type="range"
                                  min="20"
                                  max="120"
                                  value={sticker.size}
                                  onChange={(e) => {
                                    setStickers((prev) =>
                                      prev.map((s) =>
                                        s.id === selectedSticker
                                          ? {
                                              ...s,
                                              size: Number.parseInt(
                                                e.target.value
                                              ),
                                            }
                                          : s
                                      )
                                    );
                                  }}
                                  className="w-full"
                                />
                              </div>
                              <div>
                                <label className="block text-sm text-gray-400 mb-1">
                                  Start Time
                                </label>
                                <input
                                  type="number"
                                  min="0"
                                  max={effectiveTimeline.duration}
                                  step="0.1"
                                  value={sticker.startTime}
                                  onChange={(e) => {
                                    setStickers((prev) =>
                                      prev.map((s) =>
                                        s.id === selectedSticker
                                          ? {
                                              ...s,
                                              startTime: Number.parseFloat(
                                                e.target.value
                                              ),
                                            }
                                          : s
                                      )
                                    );
                                  }}
                                  className="w-full px-2 py-1 bg-gray-700 rounded text-sm"
                                />
                              </div>
                              <div>
                                <label className="block text-sm text-gray-400 mb-1">
                                  End Time
                                </label>
                                <input
                                  type="number"
                                  min={sticker.startTime}
                                  max={effectiveTimeline.duration}
                                  step="0.1"
                                  value={sticker.endTime}
                                  onChange={(e) => {
                                    setStickers((prev) =>
                                      prev.map((s) =>
                                        s.id === selectedSticker
                                          ? {
                                              ...s,
                                              endTime: Number.parseFloat(
                                                e.target.value
                                              ),
                                            }
                                          : s
                                      )
                                    );
                                  }}
                                  className="w-full px-2 py-1 bg-gray-700 rounded text-sm"
                                />
                              </div>
                            </>
                          );
                        })()}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  <h4 className="font-medium text-gray-300">
                    Available Stickers
                  </h4>
                  <div className="grid grid-cols-4 gap-3">
                    {availableStickers.map((sticker) => (
                      <button
                        key={sticker.id}
                        onClick={() =>
                          addSticker(
                            sticker,
                            setStickers,
                            setSelectedSticker,
                            effectiveTimeline
                          )
                        }
                        className="aspect-square bg-gray-700 hover:bg-gray-600 rounded-lg flex items-center justify-center text-2xl transition-colors"
                        title={sticker.name}
                      >
                        {sticker.emoji}
                      </button>
                    ))}
                  </div>

                  {stickers.length > 0 && (
                    <div className="space-y-3">
                      <h4 className="font-medium text-gray-300">
                        Added Stickers
                      </h4>
                      <div className="space-y-2">
                        {stickers.map((sticker) => (
                          <div
                            key={sticker.id}
                            className={`p-3 rounded border cursor-pointer transition-all ${
                              selectedSticker === sticker.id
                                ? "border-cyan-400 bg-cyan-900/20"
                                : "border-gray-600 bg-gray-700/30 hover:bg-gray-700/50"
                            }`}
                            onClick={() => setSelectedSticker(sticker.id)}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span className="text-lg">{sticker.emoji}</span>
                                <div className="text-sm">
                                  <div className="text-white">
                                    Sticker {sticker.id}
                                  </div>
                                  <div className="text-gray-400">
                                    {formatTime(sticker.startTime)} -{" "}
                                    {formatTime(sticker.endTime)}
                                  </div>
                                </div>
                              </div>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  deleteSticker(
                                    sticker.id,
                                    setStickers,
                                    setSelectedSticker
                                  );
                                }}
                                className="w-6 h-6 bg-red-500 hover:bg-red-600 rounded text-white text-xs flex items-center justify-center"
                              >
                                ×
                              </button>
                            </div>
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

      {/* Export Review Modal */}
      {isReviewOpen && (
        <Review
          onClose={() => {
            setIsReviewOpen(false);
            setExportData(null);
          }}
          exportData={exportData}
        />
      )}

      <style jsx>{`
        .clip-path-triangle {
          clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        }
      `}</style>
    </div>
  );
};

export default EditVideo;

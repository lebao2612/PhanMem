"use client";
import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import Review from "../components/Review";
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

  const [rightPanelTab, setRightPanelTab] = useState("details");

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
    updateEffectiveTimeline(clips, setEffectiveTimeline);
  }, [clips]);

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

  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [exportData, setExportData] = useState(null);

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
                  className="relative"
                  onClick={() => {}}
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
                        {formatTime(currentTime * 1000)}
                      </span>{" "}
                      {/* Sửa lỗi */}
                      <span className="text-gray-400 mx-2">/</span>
                      <span className="text-gray-300">
                        {formatTime(effectiveTimeline.duration * 1000)}
                      </span>{" "}
                      {/* Sửa lỗi */}
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
                        )}{" "}
                        {/* Sửa lỗi */}
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
                <div className="w-20 bg-[#2a2a2a] border-r border-gray-600 flex flex-col">
                  <div className="h-12 flex items-center justify-center border-b border-gray-600 text-xs font-medium">
                    Video
                  </div>
                  <div className="h-12 flex items-center justify-center border-b border-gray-600 text-xs font-medium text-gray-500">
                    Audio
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
                          </div>{" "}
                          {/* Sửa lỗi */}
                        </div>
                      )
                    )}
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
                            } hover:border-cyan-300`}
                          >
                            <div className="p-1 text-xs font-medium text-white truncate">
                              {clip.id || `Clip ${index + 1}`}
                            </div>
                            <div className="absolute bottom-1 left-1 text-xs text-cyan-100 font-mono">
                              {formatTime((clip.end - clip.start) * 1000)}{" "}
                              {/* Sửa lỗi */}
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
                  <div className="h-12 bg-[#1a1a1a] border-b border-gray-600 relative">
                    <div className="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">
                      Audio Track
                    </div>
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
                        <span>{formatTime(duration * 1000)}</span>{" "}
                        {/* Sửa lỗi */}
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Current Time:</span>
                        <span className="text-cyan-400">
                          {formatTime(currentTime * 1000)}
                        </span>{" "}
                        {/* Sửa lỗi */}
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
                                {formatTime((clip.end - clip.start) * 1000)}{" "}
                                {/* Sửa lỗi */}
                              </span>
                            </div>
                            <div className="text-xs text-gray-500">
                              {formatTime(clip.start * 1000)} →{" "}
                              {formatTime(clip.end * 1000)} {/* Sửa lỗi */}
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
      {isReviewOpen && (
        <Review
          onClose={() => {
            setIsReviewOpen(false);
            setExportData(null);
          }}
          exportData={exportData}
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

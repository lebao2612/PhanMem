"use client";

import { useEffect, useRef, useState, useCallback, useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import Review from "../components/Review";
import UploadVideo from "../components/UploadVideo";
import Notification from "../components/Notification"; // Đảm bảo import đúng đường dẫn
import { AuthContext } from "../contexts/AuthContext";
import {
  formatTime,
  updateEffectiveTimeline,
  handleResetTrim,
  handleUndo,
  togglePlay,
  handleTimelineClick,
  handleSave,
} from "../scripts/editVideo";
import {
  Lock,
  Eye,
  Volume2,
  MoreHorizontal,
  Play,
  Pause,
  Save,
  RotateCcw,
  X,
} from "lucide-react";

const EditVideo = () => {
  const location = useLocation();
  const videoId = location.state.videoId;
  const videoUrl = location.state.videoUrl;
  const initialGeneratedScripts = location.state?.generatedScripts || [];
  const initialGeneratedImages = location.state?.generatedImages || [];
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const timelineRef = useRef(null);
  const videoContainerRef = useRef(null);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [dragging, setDragging] = useState(null);
  const [trimStart, setTrimStart] = useState(0);
  const [trimEnd, setTrimEnd] = useState(0);
  const [history, setHistory] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [effectiveTimeline, setEffectiveTimeline] = useState({
    duration: 0,
    trimStart: 0,
    trimEnd: 0,
    originalDuration: 0,
  });
  const [rightPanelTab, setRightPanelTab] = useState("details");
  const [isReviewOpen, setIsReviewOpen] = useState(false);
  const [exportData, setExportData] = useState(null);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [uploadVideoData, setUploadVideoData] = useState(null);
  const [textToInsert, setTextToInsert] = useState("");
  const [textOverlays, setTextOverlays] = useState([]);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [selectedOverlayId, setSelectedOverlayId] = useState(null);

  // State cho notifications
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState("");
  const [notificationType, setNotificationType] = useState("success");
  const [notificationActionButton, setNotificationActionButton] =
    useState(null); // State mới cho nội dung nút hành động

  const [isSaving, setIsSaving] = useState(false);
  const { authFetch } = useContext(AuthContext);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadedMetadata = () => {
      setDuration(video.duration);
      setTrimStart(0);
      setTrimEnd(video.duration);
      setEffectiveTimeline({
        duration: video.duration,
        trimStart: 0,
        trimEnd: video.duration,
        originalDuration: video.duration,
      });
    };

    const handleTimeUpdate = () => {
      const videoCurrentTime = video.currentTime;
      if (videoCurrentTime >= trimEnd) {
        video.pause();
        setIsPlaying(false);
        return;
      }
      if (videoCurrentTime < trimStart) {
        video.currentTime = trimStart;
        return;
      }
      const effectiveTime = videoCurrentTime - trimStart;
      setCurrentTime(effectiveTime);
    };

    const handlePlay = () => {
      if (video.currentTime < trimStart) {
        video.currentTime = trimStart;
      }
      setIsPlaying(true);
    };

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
  }, [trimStart, trimEnd, effectiveTimeline]);

  useEffect(() => {
    updateEffectiveTimeline(trimStart, trimEnd, duration, setEffectiveTimeline);
  }, [trimStart, trimEnd, duration]);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!dragging || !timelineRef.current || !duration) return;
      const rect = timelineRef.current.getBoundingClientRect();
      const pos = Math.min(Math.max(e.clientX - rect.left, 0), rect.width);
      const time = (pos / rect.width) * duration;

      if (dragging.type === "playhead") {
        const clampedTime = Math.max(trimStart, Math.min(time, trimEnd));
        const effectiveTime = clampedTime - trimStart;
        setCurrentTime(effectiveTime);
        videoRef.current.currentTime = clampedTime;
      } else if (dragging.type === "trim-start") {
        const newTrimStart = Math.max(0, Math.min(time, trimEnd - 0.1));
        setTrimStart(newTrimStart);
      } else if (dragging.type === "trim-end") {
        const newTrimEnd = Math.min(duration, Math.max(time, trimStart + 0.1));
        setTrimEnd(newTrimEnd);
      }
    };

    const handleMouseUp = () => {
      if (
        dragging &&
        (dragging.type === "trim-start" || dragging.type === "trim-end")
      ) {
        setHistory((prev) => [...prev, { trimStart, trimEnd }]);
      }
      setDragging(null);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragging, duration, trimStart, trimEnd]);

  // Function để hiển thị thông báo, nhận thêm tham số actionButton
  const showNotificationMessage = useCallback(
    (message, type = "success", actionButton = null) => {
      setNotificationMessage(message);
      setNotificationType(type);
      setNotificationActionButton(() => actionButton); // Lưu hàm render nút
      setShowNotification(true);
    },
    []
  );

  // Wrapper function để gọi handleSave đã import
  const onSaveClick = useCallback(() => {
    const videoElement = videoRef.current;
    const videoWidth = videoElement ? videoElement.videoWidth : null;
    const videoHeight = videoElement ? videoElement.videoHeight : null;

    handleSave(
      authFetch,
      videoId,
      trimStart,
      trimEnd,
      textOverlays,
      setIsSaving,
      showNotificationMessage,
      { width: videoWidth, height: videoHeight },
      () => {
        // onSuccessCallback được gọi khi lưu thành công
        showNotificationMessage(
          "Video đã được lưu thành công!",
          "success",
          () => (
            <button
              onClick={() => navigate("/home")}
              className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded text-sm font-medium transition-colors"
            >
              Quay về Trang chủ
            </button>
          )
        );
      }
    );
  }, [
    authFetch,
    videoId,
    trimStart,
    trimEnd,
    textOverlays,
    showNotificationMessage,
    navigate,
  ]);

  const handleConfirmUploadFromReview = (data) => {
    setUploadVideoData({
      id: videoId,
      title: data.title,
      description: data.description,
      createdAt: new Date().toISOString(),
      exportData: data.exportData,
    });
    setIsReviewOpen(false);
    setIsUploadOpen(true);
  };

  const handleInsertText = () => {
    if (textToInsert.trim()) {
      const newTextOverlay = {
        id: `text-${Date.now()}`,
        text: textToInsert,
        x: 50,
        y: 50,
        startTime: currentTime,
        endTime: currentTime + 5,
        fontSize: 48,
        isDeleting: false,
      };
      setTextOverlays((prev) => [...prev, newTextOverlay]);
      setTextToInsert("");
      setSelectedOverlayId(newTextOverlay.id);
      console.log("Text inserted:", newTextOverlay);
    } else {
      alert("Vui lòng nhập văn bản để chèn.");
    }
  };

  const handleDeleteTextOverlay = useCallback((id) => {
    setTextOverlays((prev) => prev.filter((overlay) => overlay.id !== id));
    setSelectedOverlayId(null);
    setDragging(null);
  }, []);

  const handleDragStart = useCallback(
    (e, id, type) => {
      e.stopPropagation();
      const textElement = e.currentTarget;
      const rect = textElement.getBoundingClientRect();
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
      const currentOverlay = textOverlays.find((o) => o.id === id);
      if (currentOverlay) {
        setDragging({
          id,
          type,
          initialX: currentOverlay.x,
          initialY: currentOverlay.y,
          initialFontSize: currentOverlay.fontSize,
          initialMouseX: e.clientX,
          initialMouseY: e.clientY,
        });
      }
    },
    [textOverlays]
  );

  const handleVideoContainerMouseMove = useCallback(
    (e) => {
      if (!dragging || !videoContainerRef.current || !videoRef.current) return;
      const videoElement = videoRef.current;
      const videoRect = videoElement.getBoundingClientRect();
      const containerRect = videoContainerRef.current.getBoundingClientRect();
      const currentOverlay = textOverlays.find((o) => o.id === dragging.id);
      if (!currentOverlay) return;

      let newXPercent = currentOverlay.x;
      let newYPercent = currentOverlay.y;
      let newFontSize = currentOverlay.fontSize;
      let isInDeleteZone = false;

      if (dragging.type === "move") {
        newXPercent =
          ((e.clientX - containerRect.left - dragOffset.x) /
            containerRect.width) *
          100;
        newYPercent =
          ((e.clientY - containerRect.top - dragOffset.y) /
            containerRect.height) *
          100;
        newXPercent = Math.max(0, Math.min(100, newXPercent));
        newYPercent = Math.max(0, Math.min(100, newYPercent));
      } else if (dragging.type === "resize-br") {
        const deltaX = e.clientX - dragging.initialMouseX;
        const deltaY = e.clientY - dragging.initialMouseY;
        newFontSize = dragging.initialFontSize + (deltaX + deltaY) * 0.1;
        newFontSize = Math.max(16, Math.min(120, newFontSize));
      }

      const textCurrentX_px_relative_to_container =
        (newXPercent / 100) * containerRect.width;
      const textCurrentY_px_relative_to_container =
        (newYPercent / 100) * containerRect.height;

      const textCenterX_px_relative_to_video =
        textCurrentX_px_relative_to_container -
        (videoRect.left - containerRect.left);
      const textCenterY_px_relative_to_video =
        textCurrentY_px_relative_to_container -
        (videoRect.top - containerRect.top);

      const edgeThreshold_px = 20;
      isInDeleteZone =
        textCenterX_px_relative_to_video < edgeThreshold_px ||
        textCenterX_px_relative_to_video > videoRect.width - edgeThreshold_px ||
        textCenterY_px_relative_to_video < edgeThreshold_px ||
        textCenterY_px_relative_to_video > videoRect.height - edgeThreshold_px;

      setTextOverlays((prev) =>
        prev.map((overlay) =>
          overlay.id === dragging.id
            ? {
                ...overlay,
                x: newXPercent,
                y: newYPercent,
                fontSize: newFontSize,
                isDeleting: isInDeleteZone,
              }
            : overlay
        )
      );
    },
    [dragging, dragOffset, textOverlays]
  );

  const handleVideoContainerMouseUp = useCallback(() => {
    if (dragging) {
      setTextOverlays((prev) => {
        const updatedOverlays = prev.filter((overlay) => {
          if (overlay.id === dragging.id) {
            if (overlay.isDeleting) {
              return false;
            }
          }
          return true;
        });
        return updatedOverlays.map((overlay) => ({
          ...overlay,
          isDeleting: false,
        }));
      });
    }
    setDragging(null);
    setDragOffset({ x: 0, y: 0 });
  }, [dragging]);

  const handleVideoContainerClick = useCallback((e) => {
    if (!e.target.closest(".text-overlay-wrapper")) {
      setSelectedOverlayId(null);
    }
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
                  className="relative w-full h-full flex items-center justify-center overflow-hidden"
                  onMouseMove={handleVideoContainerMouseMove}
                  onMouseUp={handleVideoContainerMouseUp}
                  onMouseLeave={handleVideoContainerMouseUp}
                  onClick={handleVideoContainerClick}
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
                        className={`text-overlay-wrapper absolute text-white font-bold pointer-events-auto select-none transition-colors transition-opacity duration-100 ${
                          overlay.isDeleting ? "text-red-500 opacity-50" : ""
                        } ${
                          selectedOverlayId === overlay.id
                            ? "border-2 border-dashed border-white/70"
                            : ""
                        }`}
                        style={{
                          left: `${overlay.x}%`,
                          top: `${overlay.y}%`,
                          transform: "translate(-50%, -50%)",
                          textShadow: "2px 2px 4px rgba(0,0,0,0.7)",
                          zIndex: 10,
                          fontSize: `${overlay.fontSize}px`,
                          whiteSpace: "nowrap",
                          padding: "4px 8px",
                          cursor:
                            selectedOverlayId === overlay.id
                              ? "grab"
                              : "default",
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedOverlayId(overlay.id);
                        }}
                        onMouseDown={(e) => {
                          if (selectedOverlayId === overlay.id) {
                            handleDragStart(e, overlay.id, "move");
                          }
                        }}
                      >
                        {overlay.text}
                        {selectedOverlayId === overlay.id && (
                          <>
                            {/* Delete Button */}
                            <button
                              className="absolute -top-3 -right-3 bg-red-600 hover:bg-red-700 rounded-full w-6 h-6 flex items-center justify-center text-white cursor-pointer z-20"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteTextOverlay(overlay.id);
                              }}
                              title="Delete text"
                            >
                              <X className="w-4 h-4" />
                            </button>
                            {/* Resize Handle */}
                            <div
                              className="absolute -bottom-2 -right-2 w-4 h-4 bg-white border border-gray-700 rounded-full cursor-nwse-resize z-20"
                              onMouseDown={(e) =>
                                handleDragStart(e, overlay.id, "resize-br")
                              }
                            />
                          </>
                        )}
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
                  <p className="text-gray-400 text-lg">
                    Chưa có video nào được tải
                  </p>
                </div>
              )}
            </div>
            <div className="h-64 bg-[#1a1a1a] border-t border-gray-700 flex flex-col">
              <div className="flex items-center justify-between px-4 py-2 bg-[#2a2a2a] border-b border-gray-600">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() =>
                      handleResetTrim(
                        duration,
                        setTrimStart,
                        setTrimEnd,
                        setHistory
                      )
                    }
                    className="px-3 py-1.5 bg-gray-600 hover:bg-gray-700 rounded text-sm font-medium transition-colors flex items-center gap-1"
                  >
                    <RotateCcw className="w-4 h-4" />
                    Đặt lại cắt
                  </button>
                  <button
                    onClick={() =>
                      handleUndo(history, setTrimStart, setTrimEnd, setHistory)
                    }
                    className="px-3 py-1.5 bg-gray-600 hover:bg-gray-700 rounded text-sm font-medium transition-colors disabled:opacity-50"
                    disabled={history.length === 0}
                  >
                    Hoàn tác
                  </button>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-sm text-gray-400">
                    <span className="text-orange-400 mr-4">
                      Đã cắt: {formatTime((trimEnd - trimStart) * 1000)}
                    </span>
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
                    onClick={onSaveClick}
                    disabled={isSaving}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-sm font-medium transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSaving ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Đang lưu...
                      </>
                    ) : (
                      <>
                        <Save className="w-4 h-4" />
                        Lưu
                      </>
                    )}
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
                        length: Math.ceil(duration / 10) + 1,
                      },
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
                            {formatTime(i * 10 * 1000)}
                          </div>
                        </div>
                      )
                    )}
                  </div>
                  {/* Playhead */}
                  <div
                    className="absolute top-8 w-0.5 h-16 bg-white cursor-ew-resize z-30 shadow-lg"
                    style={{
                      left: `${
                        ((trimStart + currentTime) / duration) * 100 * zoom
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
                        currentTime,
                        setCurrentTime,
                        videoRef
                      )
                    }
                    style={{
                      width: `${100 * zoom}%`,
                    }}
                  >
                    {/* Grayed out areas for trimmed parts */}
                    {trimStart > 0 && (
                      <div
                        className="absolute top-1 h-14 bg-gray-800/80 border border-gray-600 rounded-l"
                        style={{
                          left: "0%",
                          width: `${(trimStart / duration) * 100}%`,
                        }}
                      >
                        <div className="p-1 text-xs text-gray-500">Đã cắt</div>
                      </div>
                    )}
                    {trimEnd < duration && (
                      <div
                        className="absolute top-1 h-14 bg-gray-800/80 border border-gray-600 rounded-r"
                        style={{
                          left: `${(trimEnd / duration) * 100}%`,
                          width: `${((duration - trimEnd) / duration) * 100}%`,
                        }}
                      >
                        <div className="p-1 text-xs text-gray-500">Đã cắt</div>
                      </div>
                    )}
                    {/* Active video area */}
                    <div
                      className="absolute top-1 h-14 bg-cyan-600/60 border-2 border-cyan-500 rounded relative"
                      style={{
                        left: `${(trimStart / duration) * 100}%`,
                        width: `${((trimEnd - trimStart) / duration) * 100}%`,
                      }}
                    >
                      <div className="p-1 text-xs font-medium text-white">
                        Video đang hoạt động
                      </div>
                      <div className="absolute bottom-1 left-1 text-xs text-cyan-100 font-mono">
                        {formatTime((trimEnd - trimStart) * 1000)}
                      </div>
                      {/* Left trim handle */}
                      <div
                        className="absolute -left-1 top-0 w-4 h-full bg-orange-500 cursor-ew-resize hover:bg-orange-400 transition-colors rounded-l flex items-center justify-center group"
                        onMouseDown={(e) => {
                          e.stopPropagation();
                          setDragging({ type: "trim-start" });
                        }}
                        title="Kéo để cắt đầu"
                      >
                        <div className="w-1 h-8 bg-white/60 rounded group-hover:bg-white/80"></div>
                      </div>
                      {/* Right trim handle */}
                      <div
                        className="absolute -right-1 top-0 w-4 h-full bg-orange-500 cursor-ew-resize hover:bg-orange-400 transition-colors rounded-r flex items-center justify-center group"
                        onMouseDown={(e) => {
                          e.stopPropagation();
                          setDragging({ type: "trim-end" });
                        }}
                        title="Kéo để cắt cuối"
                      >
                        <div className="w-1 h-8 bg-white/60 rounded group-hover:bg-white/80"></div>
                      </div>
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
                Chi tiết
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {rightPanelTab === "details" && (
                <div className="space-y-4">
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">
                      Thuộc tính Video
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Thời lượng gốc:</span>
                        <span>{formatTime(duration * 1000)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">
                          Thời lượng đã cắt:
                        </span>
                        <span className="text-orange-400">
                          {formatTime((trimEnd - trimStart) * 1000)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">
                          Thời gian hiện tại:
                        </span>
                        <span className="text-cyan-400">
                          {formatTime(currentTime * 1000)}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">Cài đặt cắt</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">
                          Thời gian bắt đầu:
                        </span>
                        <span className="text-orange-400">
                          {formatTime(trimStart * 1000)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">
                          Thời gian kết thúc:
                        </span>
                        <span className="text-orange-400">
                          {formatTime(trimEnd * 1000)}
                        </span>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500 bg-gray-800 p-2 rounded">
                      💡 Mẹo: Kéo các tay cầm màu cam trên dòng thời gian để cắt
                      video
                    </div>
                  </div>
                  {/* Text Insertion Section */}
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-300">Chèn văn bản</h4>
                    <textarea
                      placeholder="Nhập văn bản để chèn..."
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
                      Chèn văn bản
                    </button>
                  </div>
                  {/* Display current text overlays */}
                  {textOverlays.length > 0 && (
                    <div className="space-y-3 mt-6">
                      <h4 className="font-medium text-gray-300">
                        Lớp phủ văn bản đang hoạt động
                      </h4>
                      <div className="space-y-2 text-sm text-zinc-300">
                        {textOverlays.map((overlay) => (
                          <div
                            key={overlay.id}
                            className="p-2 bg-zinc-800 rounded border border-zinc-700"
                          >
                            <p className="truncate">"{overlay.text}"</p>
                            <p className="text-xs text-zinc-500">
                              Thời gian: {formatTime(overlay.startTime * 1000)}{" "}
                              - {formatTime(overlay.endTime * 1000)}
                            </p>
                            <p className="text-xs text-zinc-500">
                              Vị trí: {overlay.x.toFixed(1)}%,{" "}
                              {overlay.y.toFixed(1)}%
                            </p>
                            <p className="text-xs text-zinc-500">
                              Cỡ chữ: {overlay.fontSize.toFixed(0)}px
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
      {/* Notification */}
      {showNotification && (
        <Notification
          message={notificationMessage}
          type={notificationType}
          onClose={() => setShowNotification(false)}
          renderActionButton={notificationActionButton} // Truyền nội dung nút hành động
        />
      )}
      {isReviewOpen && (
        <Review
          onClose={() => {
            setIsReviewOpen(false);
            setExportData(null);
          }}
          exportData={exportData}
          onConfirmUpload={handleConfirmUploadFromReview}
        />
      )}
      {isUploadOpen && uploadVideoData && (
        <UploadVideo
          selectedVideo={uploadVideoData}
          onClose={() => {
            setIsUploadOpen(false);
            setUploadVideoData(null);
          }}
          onBack={() => {
            setIsUploadOpen(false);
            setIsReviewOpen(true);
          }}
          onSuccess={() => navigate("/home")}
        />
      )}
      <style>{`
        .clip-path-triangle {
          clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        }
        /* Animation cho popup giữa màn hình */
        @keyframes fade-in-scale {
          from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8);
          }
          to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
          }
        }
        .animate-fade-in-scale {
          animation: fade-in-scale 0.3s ease-out forwards;
        }
        /* Giữ lại animation slide-in nếu bạn dùng cho các mục đích khác */
        @keyframes slide-in {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default EditVideo;

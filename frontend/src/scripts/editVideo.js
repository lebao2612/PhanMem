export const formatTime = (milliseconds) => {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const ms = Math.floor((milliseconds % 1000) / 10);
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}.${ms.toString().padStart(2, "0")}`;
};

export const updateEffectiveTimeline = (
  trimStart,
  trimEnd,
  originalDuration,
  setEffectiveTimeline
) => {
  const effectiveDuration = trimEnd - trimStart;
  setEffectiveTimeline({
    duration: effectiveDuration,
    trimStart: trimStart,
    trimEnd: trimEnd,
    originalDuration: originalDuration,
  });
};

export const handleResetTrim = (
  originalDuration,
  setTrimStart,
  setTrimEnd,
  setHistory
) => {
  setHistory((prev) => [
    ...prev,
    {
      trimStart: prev.trimStart || 0,
      trimEnd: prev.trimEnd || originalDuration,
    },
  ]);
  setTrimStart(0);
  setTrimEnd(originalDuration);
};

export const handleUndo = (history, setTrimStart, setTrimEnd, setHistory) => {
  if (history.length === 0) return;
  const previousState = history[history.length - 1];
  setTrimStart(previousState.trimStart);
  setTrimEnd(previousState.trimEnd);
  setHistory((prev) => prev.slice(0, prev.length - 1));
};

export const togglePlay = (videoElement, isPlaying, setIsPlaying) => {
  if (!videoElement) return;
  if (isPlaying) {
    videoElement.pause();
  } else {
    videoElement.play();
  }
  setIsPlaying(!isPlaying);
};

export const handleTimelineClick = (
  e,
  timelineRef,
  effectiveTimeline,
  currentTime,
  setCurrentTime,
  videoRef
) => {
  const rect = timelineRef.current.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const timelineWidth = rect.width;
  const clickedTime =
    (clickX / timelineWidth) * effectiveTimeline.originalDuration;

  const effectiveTime = Math.max(
    0,
    Math.min(
      clickedTime - effectiveTimeline.trimStart,
      effectiveTimeline.duration
    )
  );
  setCurrentTime(effectiveTime);
  if (videoRef.current) {
    videoRef.current.currentTime = clickedTime;
  }
};

export const handleSave = async (
  authFetch,
  videoId,
  trimStart,
  trimEnd,
  textOverlays,
  setIsSaving,
  showNotificationMessage,
  videoDimensions,
  onSuccessCallback
) => {
  if (!videoId) {
    showNotificationMessage("Video ID is missing", "error");
    return;
  }
  setIsSaving(true);
  try {
    const requestBody = {
      trim: {
        start: trimStart,
        end: trimEnd,
      },
      theme: {
        music: {
          url: "",
          volume: 0.5,
        },
      },
      overlay: {
        stickers: [],
        texts: textOverlays.map((overlay) => ({
          text: overlay.text,
          start: overlay.startTime,
          end: overlay.endTime,
          position: [overlay.x, overlay.y],
          color: "#ffffff",
          fontSize: overlay.fontSize,
        })),
      },
      videoDimensions: videoDimensions,
    };
    console.log("Saving video with data:", requestBody);
    const response = await authFetch(`/api/videos/${videoId}`, {
      method: "PUT",
      body: JSON.stringify(requestBody),
    });
    console.log("Save successful:", response);
    // showNotificationMessage("Video has been saved successfully!", "success"); // Dòng này sẽ được xử lý bởi onSuccessCallback
    if (onSuccessCallback) {
      onSuccessCallback(); // <-- GỌI CALLBACK KHI THÀNH CÔNG
    }
  } catch (error) {
    console.error("Error saving video:", error);
    showNotificationMessage(
      error.message || "Lưu video thất bại. Vui lòng thử lại.",
      "error"
    );
  } finally {
    setIsSaving(false);
  }
};

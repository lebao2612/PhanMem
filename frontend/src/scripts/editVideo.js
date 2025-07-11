// scripts/editVideo.js

export const formatTime = (milliseconds) => {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const ms = Math.floor((milliseconds % 1000) / 10);
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}.${ms.toString().padStart(2, "0")}`;
};

export const updateEffectiveTimeline = (clips, setEffectiveTimeline) => {
  let totalEffectiveDuration = 0;
  const segments = [];

  clips.forEach((clip) => {
    const clipDuration = clip.end - clip.start;
    totalEffectiveDuration += clipDuration;
    segments.push({
      start: segments.length > 0 ? segments[segments.length - 1].end : 0,
      end:
        (segments.length > 0 ? segments[segments.length - 1].end : 0) +
        clipDuration,
      originalStart: clip.start,
      originalEnd: clip.end,
    });
  });

  setEffectiveTimeline({
    duration: totalEffectiveDuration,
    segments: segments,
  });
};

export const handleSplitVideo = (
  currentTime,
  effectiveTimeline,
  clips,
  setClips,
  setHistory,
  setSelectedClipIndex
) => {
  setHistory((prev) => [...prev, clips]); // Save current state for undo

  let originalSplitTime = 0;
  let accumulatedEffectiveDuration = 0;
  for (const segment of effectiveTimeline.segments) {
    const segmentEffectiveDuration = segment.end - segment.start;
    if (
      currentTime >= accumulatedEffectiveDuration &&
      currentTime < accumulatedEffectiveDuration + segmentEffectiveDuration
    ) {
      originalSplitTime =
        segment.originalStart + (currentTime - accumulatedEffectiveDuration);
      break;
    }
    accumulatedEffectiveDuration += segmentEffectiveDuration;
  }

  const newClips = [];
  let splitPerformed = false;

  clips.forEach((clip, index) => {
    if (originalSplitTime > clip.start && originalSplitTime < clip.end) {
      // Split this clip
      const firstPart = {
        ...clip,
        end: originalSplitTime,
        id: `clip-${Date.now()}-${index}-a`,
      };
      const secondPart = {
        ...clip,
        start: originalSplitTime,
        id: `clip-${Date.now()}-${index}-b`,
      };
      newClips.push(firstPart, secondPart);
      splitPerformed = true;
    } else {
      newClips.push(clip);
    }
  });

  if (splitPerformed) {
    setClips(newClips);
    setSelectedClipIndex(null); // Deselect after split
  } else {
    // If no split occurred (e.g., current time is at a clip boundary), revert history
    setHistory((prev) => prev.slice(0, prev.length - 1));
  }
};

export const handleDeleteClip = (
  selectedClipIndex,
  clips,
  setClips,
  setHistory,
  setSelectedClipIndex
) => {
  if (selectedClipIndex === null) return;

  setHistory((prev) => [...prev, clips]); // Save current state for undo

  const newClips = clips.filter((_, index) => index !== selectedClipIndex);
  setClips(newClips);
  setSelectedClipIndex(null); // Deselect after deletion
};

export const handleUndo = (
  history,
  setClips,
  setHistory,
  setSelectedClipIndex,
  setSelectionRange
) => {
  if (history.length === 0) return;

  const previousState = history[history.length - 1];
  setClips(previousState);
  setHistory((prev) => prev.slice(0, prev.length - 1));
  setSelectedClipIndex(null);
  setSelectionRange(null);
};

export const togglePlay = (
  videoElement,
  isPlaying,
  setIsPlaying,
  currentTime
) => {
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
  totalEffectiveDuration,
  currentTime,
  setCurrentTime,
  setSelectionRange,
  videoRef,
  clips,
  setSelectedClipIndex
) => {
  const rect = timelineRef.current.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const timelineWidth = rect.width;

  const clickedEffectiveTime =
    (clickX / timelineWidth) * totalEffectiveDuration;

  let originalVideoTime = 0;
  let accumulatedEffectiveDuration = 0;
  for (const segment of effectiveTimeline.segments) {
    const segmentEffectiveDuration = segment.end - segment.start;
    if (
      clickedEffectiveTime >= accumulatedEffectiveDuration &&
      clickedEffectiveTime <
        accumulatedEffectiveDuration + segmentEffectiveDuration
    ) {
      originalVideoTime =
        segment.originalStart +
        (clickedEffectiveTime - accumulatedEffectiveDuration);
      break;
    }
    accumulatedEffectiveDuration += segmentEffectiveDuration;
  }

  setCurrentTime(clickedEffectiveTime);
  if (videoRef.current) {
    videoRef.current.currentTime = originalVideoTime;
  }

  const clickedClipIndex = clips.findIndex(
    (clip) =>
      clickedEffectiveTime >= clip.start && clickedEffectiveTime <= clip.end
  );
  setSelectedClipIndex(clickedClipIndex !== -1 ? clickedClipIndex : null);

  setSelectionRange(null);
};

export const processVideoForExport = (videoUrl, clips, effectiveTimeline) => {
  const exportSummary = {
    originalVideoUrl: videoUrl,
    clipsToExport: clips.map((clip) => ({
      start: formatTime(clip.start * 1000), // Sửa lỗi
      end: formatTime(clip.end * 1000), // Sửa lỗi
      duration: formatTime((clip.end - clip.start) * 1000), // Sửa lỗi
    })),
    totalExportDuration: formatTime(effectiveTimeline.duration * 1000), // Sửa lỗi
    previewUrl: videoUrl,
  };

  console.log("Export Data:", exportSummary);
  return exportSummary;
};

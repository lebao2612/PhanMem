export const formatTime = (time) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  const milliseconds = Math.floor((time % 1) * 100);
  return `${minutes}:${seconds.toString().padStart(2, "0")}.${milliseconds
    .toString()
    .padStart(2, "0")}`;
};

export const updateEffectiveTimeline = (newClips, setEffectiveTimeline) => {
  const sortedClips = [...newClips].sort((a, b) => a.start - b.start);
  let effectiveTime = 0;
  const segments = [];

  sortedClips.forEach((clip) => {
    const duration = clip.end - clip.start;
    segments.push({
      start: effectiveTime,
      end: effectiveTime + duration,
      originalStart: clip.start,
      originalEnd: clip.end,
    });
    effectiveTime += duration;
  });

  setEffectiveTimeline({
    duration: effectiveTime,
    segments: segments,
  });
};

export const addSticker = (
  stickerType,
  setStickers,
  setSelectedSticker,
  effectiveTimeline
) => {
  const newSticker = {
    id: Date.now(),
    type: stickerType.id,
    emoji: stickerType.emoji,
    x: 50 + (Math.random() - 0.5) * 20,
    y: 50 + (Math.random() - 0.5) * 20,
    size: 60,
    rotation: 0,
    startTime: 0,
    endTime: effectiveTimeline.duration,
  };
  setStickers((prev) => [...prev, newSticker]);
  setSelectedSticker(newSticker.id);

  setTimeout(() => {
    setStickers((prev) =>
      prev.map((s) => (s.id === newSticker.id ? { ...s, size: s.size } : s))
    );
  }, 50);
};

export const deleteSticker = (stickerId, setStickers, setSelectedSticker) => {
  setStickers((prev) => prev.filter((s) => s.id !== stickerId));
  setSelectedSticker(null);
};

export const handleSplitVideo = (
  currentTime,
  effectiveTimeline,
  clips,
  setClips,
  setHistory,
  setSelectedClipIndex
) => {
  let originalTime = currentTime;
  let accumulatedTime = 0;

  for (const segment of effectiveTimeline.segments) {
    const segmentDuration = segment.end - segment.start;
    if (
      currentTime >= accumulatedTime &&
      currentTime <= accumulatedTime + segmentDuration
    ) {
      originalTime = segment.originalStart + (currentTime - accumulatedTime);
      break;
    }
    accumulatedTime += segmentDuration;
  }

  const currentClip = clips.find(
    (clip) => originalTime >= clip.start && originalTime <= clip.end
  );
  if (
    !currentClip ||
    originalTime <= currentClip.start ||
    originalTime >= currentClip.end
  )
    return;

  setHistory((prev) => [...prev, clips]);

  setClips((prevClips) => {
    const newClips = [];
    for (let i = 0; i < prevClips.length; i++) {
      const clip = prevClips[i];
      if (clip === currentClip) {
        newClips.push({
          ...clip,
          id: `${clip.id}-1`,
          end: originalTime,
        });
        newClips.push({
          ...clip,
          id: `${clip.id}-2`,
          start: originalTime,
        });
      } else {
        newClips.push(clip);
      }
    }
    updateEffectiveTimeline(newClips, setClips);
    return newClips;
  });
  setSelectedClipIndex(null);
};

export const handleDeleteSelection = (
  selectionRange,
  clips,
  setClips,
  setHistory,
  setSelectionRange,
  setSelectedClipIndex,
  updateEffectiveTimeline
) => {
  if (!selectionRange) return;

  setHistory((prev) => [...prev, clips]);

  const newClips = [];
  clips.forEach((clip) => {
    if (clip.end <= selectionRange.start || clip.start >= selectionRange.end) {
      newClips.push(clip);
    } else if (
      clip.start < selectionRange.start &&
      clip.end > selectionRange.end
    ) {
      newClips.push(
        { ...clip, id: `${clip.id}-before`, end: selectionRange.start },
        { ...clip, id: `${clip.id}-after`, start: selectionRange.end }
      );
    } else if (
      clip.start < selectionRange.start &&
      clip.end > selectionRange.start
    ) {
      newClips.push({ ...clip, end: selectionRange.start });
    } else if (
      clip.start < selectionRange.end &&
      clip.end > selectionRange.end
    ) {
      newClips.push({ ...clip, start: selectionRange.end });
    }
  });

  setClips(newClips);
  updateEffectiveTimeline(newClips, setClips);
  setSelectionRange(null);
  setSelectedClipIndex(null);
};

export const handleDeleteClip = (
  selectedClipIndex,
  clips,
  setClips,
  setHistory,
  setSelectedClipIndex,
  updateEffectiveTimeline
) => {
  if (selectedClipIndex === null) return;

  setHistory((prev) => [...prev, clips]);

  setClips((prev) => {
    const newClips = prev.filter((_, idx) => idx !== selectedClipIndex);
    updateEffectiveTimeline(newClips, setClips);
    return newClips;
  });

  setSelectedClipIndex(null);
};

export const handleUndo = (
  history,
  setClips,
  setHistory,
  setSelectedClipIndex,
  setSelectionRange
) => {
  if (history.length === 0) return;
  const previous = history[history.length - 1];
  setClips(previous);
  setHistory((prev) => prev.slice(0, -1));
  setSelectedClipIndex(null);
  setSelectionRange(null);
};

export const togglePlay = (video, isPlaying, setIsPlaying, currentTime) => {
  if (!video) return;

  if (isPlaying) {
    video.pause();
  } else {
    video.currentTime = currentTime;
    video.play();
  }
  setIsPlaying(!isPlaying);
};

export const handleTimelineClick = (
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
) => {
  if (!timelineRef.current || !effectiveTimeline.duration) return;

  const rect = timelineRef.current.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const clickedEffectiveTime =
    (clickX / rect.width) * effectiveTimeline.duration;

  if (e.shiftKey && selectionRange) {
    setSelectionRange({
      start: Math.min(selectionRange.start, clickedEffectiveTime),
      end: Math.max(selectionRange.end, clickedEffectiveTime),
    });
  } else if (e.shiftKey) {
    setSelectionRange({
      start: Math.min(currentTime, clickedEffectiveTime),
      end: Math.max(currentTime, clickedEffectiveTime),
    });
  } else {
    let originalTime = 0;
    let accumulatedTime = 0;

    for (const segment of effectiveTimeline.segments) {
      const segmentDuration = segment.end - segment.start;
      if (
        clickedEffectiveTime >= accumulatedTime &&
        clickedEffectiveTime <= accumulatedTime + segmentDuration
      ) {
        originalTime =
          segment.originalStart + (clickedEffectiveTime - accumulatedTime);
        break;
      }
      accumulatedTime += segmentDuration;
    }

    setCurrentTime(clickedEffectiveTime);
    videoRef.current.currentTime = originalTime;
    setSelectionRange(null);

    const clickedIndex = clips.findIndex((clip) => {
      let clipEffectiveStart = 0;
      let clipEffectiveEnd = 0;
      let accTime = 0;

      for (const segment of effectiveTimeline.segments) {
        const segmentDuration = segment.end - segment.start;
        if (
          segment.originalStart === clip.start &&
          segment.originalEnd === clip.end
        ) {
          clipEffectiveStart = accTime;
          clipEffectiveEnd = accTime + segmentDuration;
          break;
        }
        accTime += segmentDuration;
      }

      return (
        clickedEffectiveTime >= clipEffectiveStart &&
        clickedEffectiveTime <= clipEffectiveEnd
      );
    });
    setSelectedClipIndex(clickedIndex !== -1 ? clickedIndex : null);
  }
};

export const processVideoForExport = (
  videoUrl,
  clips,
  stickers,
  effectiveTimeline
) => {
  const exportData = {
    originalVideoUrl: videoUrl,
    clips: clips.map((clip, index) => ({
      id: clip.id || `clip-${index}`,
      startTime: clip.start,
      endTime: clip.end,
      duration: clip.end - clip.start,
    })),
    stickers: stickers.map((sticker) => ({
      id: sticker.id,
      emoji: sticker.emoji,
      x: sticker.x,
      y: sticker.y,
      size: sticker.size,
      rotation: sticker.rotation,
      startTime: sticker.startTime,
      endTime: sticker.endTime,
    })),
    timeline: {
      totalDuration: effectiveTimeline.duration,
      segments: effectiveTimeline.segments,
    },
  };

  return exportData;
};

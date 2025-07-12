// API service for video processing
export const processVideoWithAPI = async (videoId, editData) => {
  try {
    const response = await fetch(`/api/videos/${videoId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editData),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error processing video:", error);
    throw error;
  }
};

// Convert your current edit data to API format
export const convertToAPIFormat = (
  clips,
  textOverlays,
  effectiveTimeline,
  videoId
) => {
  // Calculate trim based on clips
  const firstClip = clips[0];
  const lastClip = clips[clips.length - 1];

  const apiData = {
    trim: {
      start: firstClip ? firstClip.start : 0,
      end: lastClip ? lastClip.end : effectiveTimeline.duration,
    },
    theme: {
      music: {
        url: "", // You can add music URL here if needed
        volume: 0.5,
      },
    },
    overlay: {
      stickers: [], // You can add stickers here if needed
      texts: textOverlays.map((overlay) => ({
        text: overlay.text,
        start: overlay.startTime,
        end: overlay.endTime,
        position: [overlay.x, overlay.y],
        color: "#ffffff", // Default white color, you can make this configurable
      })),
    },
  };

  return apiData;
};

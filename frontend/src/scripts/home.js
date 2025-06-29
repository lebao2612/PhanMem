export const handlePressMenu = (menuOpen, setMenuOpen) => () => {
  setMenuOpen(!menuOpen);
};

export const countInputWord = (setWordCount) => (event) => {
  const text = event.target.value;
  setWordCount(text.length);
};

export const handleInput = (e, setText, textareaRef) => {
  const value = e.target.value;
  if (value.length <= 200) {
    setText(value);
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    }
  }
};

export const handleFetchTrendingTopics = async (
  authFetch,
  setTrendingTopics,
  setShowTrendingPopup,
  setIsLoadingTrending
) => {
  try {
    setIsLoadingTrending(true);
    const res = await authFetch("/api/generators/topic/trending");
    setTrendingTopics(res);
    setShowTrendingPopup(true);
  } catch (err) {
    console.error("Lỗi khi gọi API trending topics:", err.message);
  } finally {
    setIsLoadingTrending(false);
  }
};

export const handleFetchSuggestedTopics = async (
  text,
  authFetch,
  setSuggestedTopics,
  setShowSuggestedPopup,
  setIsLoadingSuggested
) => {
  if (!text.trim()) {
    alert("Please enter a topic before fetching suggestions.");
    return;
  }

  try {
    setIsLoadingSuggested(true);
    const res = await authFetch(
      `/api/generators/topic/suggestions?query=${encodeURIComponent(text)}`
    );
    setSuggestedTopics(res);
    setShowSuggestedPopup(true);
  } catch (err) {
    console.error("Lỗi khi gọi API suggested topics:", err.message);
  } finally {
    setIsLoadingSuggested(false);
  }
};
export const handleGenerateScript = async (
  text,
  authFetch,
  setGeneratedScript,
  setShowScriptArea,
  setScriptError,
  setVideoId // Có thể bỏ luôn nếu không dùng nữa
) => {
  if (!text.trim()) {
    alert("Please enter a topic before generating script.");
    return false;
  }

  try {
    // Gọi API sinh script từ topic
    const scriptRes = await authFetch("/api/generators/script", {
      method: "POST",
      body: JSON.stringify({ topic: text }),
    });

    const script = typeof scriptRes === "string" ? scriptRes : scriptRes.script;

    console.log("📥 Script API response:", scriptRes);
    // Cập nhật giao diện
    setGeneratedScript(script);
    setShowScriptArea(true);
    setScriptError(false);

    return true;
  } catch (error) {
    console.error("Lỗi khi sinh script:", error.message);
    alert("Đã xảy ra lỗi khi tạo script. Hãy thử lại.");
    return false;
  }
};

// Hàm này sẽ gọi API để sinh voice từ script đã tạo
export const handleGenerateVoice = async (
  generatedScript,
  setVoiceUrl,
  setIsLoadingVoice
) => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Token không tồn tại. Vui lòng đăng nhập lại.");
    return;
  }

  setIsLoadingVoice(true);
  setVoiceUrl("");

  console.log("📤 Gửi script đến API voice:", generatedScript);
  // Giả sử nhận voice_url từ backend
  const voice_url =
    "https://res.cloudinary.com/df8meqyyc/video/upload/v1750859823/tts-audio/qfv6ryugzwx5hlqltvgz.mp3";
  console.log("📥 Nhận voice_url:", voice_url);
  setVoiceUrl(voice_url);
  setIsLoadingVoice(false);

  // ------------- Chưa dùng được API (Thiếu secret key) -------------
  // Nếu backend đã sẵn sàng, có thể bỏ comment đoạn này để gọi API

  // try {
  //   const res = await fetch("/api/generators/voice", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: `Bearer ${token}`,
  //     },
  //     body: JSON.stringify({ script: generatedScript }), // ✅ đúng format backend yêu cầu
  //   });

  //   if (!res.ok) {
  //     const err = await res.json();
  //     throw new Error(err?.error || "Lỗi khi gọi API voice.");
  //   }

  //   const data = await res.json();
  //   console.log("📥 Voice API response:", data);

  //   if (data.voice_url) {
  //     setVoiceUrl(data.voice_url);
  //   } else {
  //     console.warn("⚠️ Không có voice_url trong response:", data);
  //     alert("Không tìm thấy voice_url trong phản hồi.");
  //   }
  // } catch (error) {
  //   console.error("Voice generation error:", error.message);
  //   alert("Đã xảy ra lỗi khi gọi API voice.");
  // } finally {
  //   setIsLoadingVoice(false);
  // }
};

// Hàm này sẽ gọi API để sinh video từ voice đã tạo
// scripts/home.js
export const handleGenerateVideo = async (
  videoId,
  authFetch,
  setVideoUrl,
  setIsLoadingVideo
) => {
  // // if (!videoId) return;
  // if (!videoId || videoId.trim() === "") {
  //   alert("Please provide a valid video ID.");
  //   return;
  // }

  setIsLoadingVideo(true);
  setVideoUrl("");

  // Giả sử nhận video_url từ backend
  const videoUrl =
    "https://res.cloudinary.com/dznocieoi/video/upload/v1751044595/video_utej9c.mp4";
  const videoUrl2 =
    "https://res.cloudinary.com/dznocieoi/video/upload/v1751080891/videoplayback_rgkq72.mp4";
  console.log("Url video:", videoUrl, videoUrl2);
  setVideoUrl(videoUrl2);
  setIsLoadingVideo(false);

  // Chưa dùng được API (Thiếu videoID)
  // try {
  //   const response = await authFetch("/api/generators/video", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ video_id: videoId }),
  //   });

  //   if (!response.ok) throw new Error("Video generation failed");

  //   const data = await response.json();
  //   setVideoUrl(data.video_url); //  Backend trả về `video_url` trong `VideoDTO`
  // } catch (err) {
  //   console.error("Video generation error:", err);
  // } finally {
  //   setIsLoadingVideo(false);
  // }
};

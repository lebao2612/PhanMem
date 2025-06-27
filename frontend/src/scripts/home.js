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

    const script = scriptRes.script;

    // Cập nhật giao diện
    setGeneratedScript(script);
    setShowScriptArea(true);
    setScriptError(false);
    // setVideoId không dùng nữa => có thể bỏ dòng dưới
    // setVideoId(null);

    return true;
  } catch (error) {
    console.error("Lỗi khi sinh script:", error.message);
    alert("Đã xảy ra lỗi khi tạo script. Hãy thử lại.");
    return false;
  }
};

export const handleGenerateVoice = async (
  videoId,
  _authFetch,
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

  try {
    const res = await fetch("/api/generators/voice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ video_id: videoId }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err?.error || "Lỗi khi gọi API voice.");
    }

    const data = await res.json();
    console.log("📥 Voice API response:", data);

    if (data.voice_url) {
      setVoiceUrl(data.voice_url);
    } else {
      console.warn("⚠️ Không có voice_url trong response:", data);
      alert("Không tìm thấy voice_url trong phản hồi.");
    }
  } catch (error) {
    console.error("Voice generation error:", error.message);
    alert("Đã xảy ra lỗi khi gọi API voice.");
  } finally {
    setIsLoadingVoice(false);
  }
};

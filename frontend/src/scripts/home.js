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
  setGeneratedScripts, // Changed from setGeneratedScript
  setShowScriptArea,
  setScriptError,
  setVideoId
) => {
  if (!text.trim()) {
    alert("Please enter a topic before generating script.");
    return false;
  }
  try {
    // Call API to generate script from topic
    const scriptRes = await authFetch("/api/generators/script", {
      method: "POST",
      body: JSON.stringify({ topic: text }),
    });

    console.log("📥 Script API response:", scriptRes);

    // Handle the response - assuming it returns an object with a script array
    let scriptArray = [];
    if (Array.isArray(scriptRes)) {
      scriptArray = scriptRes;
    } else if (scriptRes.script && Array.isArray(scriptRes.script)) {
      scriptArray = scriptRes.script;
    } else if (typeof scriptRes === "string") {
      // If it's a string, create a single script object
      scriptArray = [{ label: "Scene 1", subtitle: scriptRes }];
    }

    // Update UI with script array
    setGeneratedScripts(scriptArray);
    setShowScriptArea(true);
    setScriptError(false);
    return true;
  } catch (error) {
    console.error("Lỗi khi sinh script:", error.message);
    alert("Đã xảy ra lỗi khi tạo script. Hãy thử lại.");
    return false;
  }
};

// This function will call API to generate voice from created script
export const handleGenerateVoice = async (
  generatedScripts, // Changed to accept the full scripts array instead of combined text
  setVoiceUrl,
  setIsLoadingVoice,
  videoId = "", // Add videoId parameter
  voiceGender = "female" // Add voiceGender parameter with default
) => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Token không tồn tại. Vui lòng đăng nhập lại.");
    return;
  }

  setIsLoadingVoice(true);
  setVoiceUrl("");
  console.log("📤 Gửi script đến API voice:", generatedScripts);

  // Mock voice URL from backend
  const mockVoiceUrl = "https://res.cloudinary.com/demo/video/upload/dog.mp3";
  setVoiceUrl(mockVoiceUrl);
  setIsLoadingVoice(false);

  // try {
  //   const requestBody = {
  //     videoId: videoId,
  //     script: generatedScripts, // Send the full script array
  //     voiceGender: voiceGender,
  //   }

  //   console.log("📤 Request body:", JSON.stringify(requestBody, null, 2))
  //   console.log("📤 Request URL: /api/generators/voice")
  //   console.log("📤 Token:", token ? "Present" : "Missing")

  //   const res = await fetch("/api/generators/voice", {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: `Bearer ${token}`,
  //     },
  //     body: JSON.stringify(requestBody),
  //   })

  //   console.log("📥 Response status:", res.status)
  //   console.log("📥 Response headers:", Object.fromEntries(res.headers.entries()))

  //   if (!res.ok) {
  //     if (res.status === 404) {
  //       console.error("❌ API endpoint not found. Check if:")
  //       console.error("1. Backend server is running")
  //       console.error("2. Endpoint URL is correct: /api/generators/voice")
  //       console.error("3. Route is implemented in backend")
  //       alert("API endpoint không tồn tại. Vui lòng kiểm tra backend server.")
  //       return
  //     }

  //     let errorMessage = "Unknown error"
  //     try {
  //       const err = await res.json()
  //       errorMessage = err?.error || err?.message || `HTTP ${res.status}`
  //     } catch (parseError) {
  //       errorMessage = `HTTP ${res.status} - ${res.statusText}`
  //     }

  //     throw new Error(errorMessage)
  //   }

  //   const response = await res.json()
  //   console.log("📥 Voice API response:", response)

  //   // Handle the new response structure
  //   if (response.success && response.data && response.data.voiceUrl) {
  //     setVoiceUrl(response.data.voiceUrl)
  //     console.log("✅ Voice URL set successfully:", response.data.voiceUrl)
  //   } else {
  //     console.warn("⚠️ Không có voiceUrl trong response:", response)
  //     alert("Không tìm thấy voiceUrl trong phản hồi.")
  //   }
  // } catch (error) {
  //   console.error("❌ Voice generation error:", error.message)

  //   // More specific error messages
  //   if (error.message.includes("fetch")) {
  //     alert("Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng.")
  //   } else if (error.message.includes("404")) {
  //     alert("API endpoint không tồn tại. Vui lòng liên hệ admin.")
  //   } else {
  //     alert(`Lỗi khi tạo voice: ${error.message}`)
  //   }
  // } finally {
  //   setIsLoadingVoice(false)
  // }
};

// This function will call API to generate video from created voice
export const handleGenerateVideo = async (
  videoId,
  authFetch,
  setVideoUrl,
  setIsLoadingVideo,
  generatedScripts, // Added to get script count for images
  setGeneratedImages // Added to set image URLs
) => {
  setIsLoadingVideo(true);
  setVideoUrl("");
  setGeneratedImages([]); // Clear previous images

  // Mock video URLs from backend
  const videoUrl =
    "https://res.cloudinary.com/dznocieoi/video/upload/v1751044595/video_utej9c.mp4";
  const videoUrl2 =
    "https://res.cloudinary.com/dznocieoi/video/upload/v1751080891/videoplayback_rgkq72.mp4";
  console.log("Url video:", videoUrl, videoUrl2);
  setVideoUrl(videoUrl2);

  // Generate mock image URLs based on the number of scripts
  const singleMockImageUrl =
    "https://res.cloudinary.com/dznocieoi/image/upload/v1752220874/Screenshot_2025-07-11_145645_kirjqe.png";
  const mockImageUrls = generatedScripts.map(() => singleMockImageUrl);
  setGeneratedImages(mockImageUrls);

  setIsLoadingVideo(false);
  // API call when ready (uncomment when backend is ready)
  // try {
  //   const response = await authFetch("/api/generators/video", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ video_id: videoId }),
  //   });
  //   if (!response.ok) throw new Error("Video generation failed");
  //   const data = await response.json();
  //   // setVideoUrl(data.video_url);
  // } catch (err) {
  //   console.error("Video generation error:", err);
  // } finally {
  //   setIsLoadingVideo(false);
  // }
};

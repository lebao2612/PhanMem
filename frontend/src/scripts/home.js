// scripts/home.js
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
  setGeneratedScripts,
  setShowScriptArea,
  setScriptError,
  setVideoId
) => {
  if (!text.trim()) {
    alert("Please enter a topic before generating script.");
    return false;
  }
  try {
    const scriptRes = await authFetch("/api/generators/script", {
      method: "POST",
      body: JSON.stringify({ topic: text }),
    });
    console.log("📥 Script API response:", scriptRes);
    let scriptArray = [];
    if (Array.isArray(scriptRes)) {
      scriptArray = scriptRes;
    } else if (scriptRes.script && Array.isArray(scriptRes.script)) {
      scriptArray = scriptRes.script;
    } else if (typeof scriptRes === "string") {
      scriptArray = [{ label: "Scene 1", subtitle: scriptRes }];
    }
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

export const handleGenerateVoice = async (
  generatedScripts,
  setGeneratedVoices, // Renamed from setVoiceUrls
  setIsLoadingVoice,
  videoId = "",
  voiceGender = "female"
) => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Token không tồn tại. Vui lòng đăng nhập lại.");
    return;
  }
  setIsLoadingVoice(true);
  setGeneratedVoices([]); // Clear previous voices
  try {
    const subtitles = generatedScripts
      .map((script) =>
        typeof script === "string"
          ? script
          : script.subtitle || script.text || ""
      )
      .filter((text) => text.trim() !== "");

    const requestBody = {
      subtitles: subtitles,
      voiceGender: voiceGender,
      voiceLanguage: "vi",
    };

    console.log("📤 Request body:", JSON.stringify(requestBody, null, 2));

    const res = await fetch("/api/generators/voices", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestBody),
    });

    if (!res.ok) {
      if (res.status === 422) {
        console.error("❌ Request body validation failed");
        alert("Dữ liệu gửi lên không đúng format. Vui lòng kiểm tra lại.");
        return;
      }
      let errorMessage = "Unknown error";
      try {
        const err = await res.json();
        errorMessage = err?.error || err?.message || `HTTP ${res.status}`;
      } catch (parseError) {
        errorMessage = `HTTP ${res.status} - ${res.statusText}`;
      }
      throw new Error(errorMessage);
    }

    const response = await res.json();
    console.log("📥 Voice API response:", response);

    let parsedVoiceData = [];
    if (response.success && response.data) {
      if (Array.isArray(response.data)) {
        if (response.data.length > 0) {
          // Ensure we store both publicId and url
          if (
            typeof response.data[0] === "object" &&
            typeof response.data[0].url === "string" &&
            typeof response.data[0].publicId === "string"
          ) {
            parsedVoiceData = response.data.map((item) => ({
              publicId: item.publicId,
              url: item.url,
            }));
          } else if (typeof response.data[0] === "string") {
            // Fallback for direct URL strings, publicId will be empty
            parsedVoiceData = response.data.map((url) => ({
              publicId: "",
              url: url.trim(),
            }));
          }
        }
      } else if (typeof response.data === "string") {
        // Fallback for single URL string, publicId will be empty
        parsedVoiceData = [{ publicId: "", url: response.data.trim() }];
      }
    }

    if (parsedVoiceData.length > 0) {
      setGeneratedVoices(parsedVoiceData); // Use setGeneratedVoices
      console.log("✅ Voice data set successfully:", parsedVoiceData);
    } else {
      console.warn("⚠️ Không có voice URLs hợp lệ trong response:", response);
      alert("Không tìm thấy voice URLs hợp lệ trong phản hồi.");
    }
  } catch (error) {
    console.error("❌ Voice generation error:", error.message);
    alert(`Lỗi khi tạo voice: ${error.message}`);
  } finally {
    setIsLoadingVoice(false);
  }
};

export const handleGenerateImages = async (
  generatedScripts,
  authFetch,
  setGeneratedImages,
  setIsLoadingImages
) => {
  if (generatedScripts.length === 0) {
    alert("Please generate a script first before generating images.");
    return;
  }

  setIsLoadingImages(true);
  setGeneratedImages([]); // Clear previous images

  try {
    const labels = generatedScripts.map((script) => script.label); // Extract labels from scripts
    const requestBody = {
      labels: labels,
    };

    const responseData = await authFetch("/api/generators/images", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    console.log("📥 Image API response:", responseData);

    let parsedImageData = [];
    if (responseData) {
      if (Array.isArray(responseData)) {
        if (responseData.length > 0) {
          // Map over the array and extract 'url' and 'publicId' from each object
          parsedImageData = responseData
            .map((item) =>
              typeof item === "object" &&
              typeof item.url === "string" &&
              typeof item.publicId === "string"
                ? { publicId: item.publicId, url: item.url }
                : null
            )
            .filter(Boolean); // Remove any nulls (items without valid data)
        }
      }
      // This case is less likely for multiple images but kept for robustness
      else if (typeof responseData === "string") {
        parsedImageData = [{ publicId: "", url: responseData.trim() }]; // PublicId will be empty
      }
    }

    if (parsedImageData.length > 0) {
      setGeneratedImages(parsedImageData);
      console.log("✅ Image data set successfully:", parsedImageData);
    } else {
      console.warn(
        "⚠️ Không có image URLs hợp lệ trong response:",
        responseData
      );
      alert("Không tìm thấy image URLs hợp lệ trong phản hồi.");
    }
  } catch (error) {
    console.error("❌ Image generation error:", error.message);
    alert(`Lỗi khi tạo hình ảnh: ${error.message}`);
  } finally {
    setIsLoadingImages(false);
  }
};

export const handleGenerateVideo = async (
  text, // Added text for title/topic
  authFetch,
  setVideoUrl,
  setIsLoadingVideo,
  generatedScripts,
  generatedVoices, // Changed from voiceUrls
  generatedImages,
  navigate // Added navigate function
) => {
  setIsLoadingVideo(true);
  setVideoUrl("");
  try {
    if (
      generatedScripts.length === 0 ||
      generatedVoices.length === 0 ||
      generatedImages.length === 0
    ) {
      alert("Please generate script, voice, and images first.");
      setIsLoadingVideo(false);
      return;
    }

    const scenes = generatedScripts.map((script, index) => {
      const voiceData = generatedVoices[index] || { publicId: "", url: "" };
      const imageData = generatedImages[index] || { publicId: "", url: "" };
      return {
        label: script.label,
        subtitle: script.subtitle,
        voice: {
          publicId: voiceData.publicId,
          url: voiceData.url,
        },
        image: {
          publicId: imageData.publicId,
          url: imageData.url,
        },
        effect: {
          zoom: "in", // Default effect, can be made dynamic
          pan: "left", // Default effect, can be made dynamic
        },
      };
    });

    const requestBody = {
      title: text, // Using the input text as the video title
      topic: text, // Using the input text as the video topic
      scenes: scenes,
    };

    console.log(
      "📤 Request body for video generation:",
      JSON.stringify(requestBody, null, 2)
    );

    // Mock API call for video generation
    const videoMockUrl =
      "https://res.cloudinary.com/prod/video/upload/w_400/me/tx-cards/trim-video.mp4";
    setVideoUrl(videoMockUrl); // Set mock video URL for testing

    // Navigate to edit-video page with all generated data
    navigate("/edit-video", {
      state: {
        videoUrl: videoMockUrl, // Use the mock URL for navigation
        generatedScripts,
        generatedVoices,
        generatedImages,
      },
    });

    // const response = await authFetch("/api/generators/video", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(requestBody),
    // });
    // console.log("📥 Video API response:", response);

    // if (response) {
    //   setVideoUrl(response.url);
    //   console.log("✅ Video URL set successfully:", response.url);
    //   // Navigate to edit-video page with all generated data
    //   navigate("/edit-video", {
    //     state: {
    //       videoUrl: response.url,
    //       generatedScripts,
    //       generatedVoices,
    //       generatedImages,
    //     },
    //   });
    // } else {
    //   console.warn("⚠️ Không có video URL hợp lệ trong response:", response);
    //   alert("Không tìm thấy video URL hợp lệ trong phản hồi.");
    // }
  } catch (error) {
    console.error("❌ Video generation error:", error.message);
    alert(`Lỗi khi tạo video: ${error.message}`);
  } finally {
    setIsLoadingVideo(false);
  }
};

"use client";
import { useContext, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import {
  FiSend,
  FiTrendingUp,
  FiPlay,
  FiPause,
  FiLoader,
} from "react-icons/fi"; // Import FiPause
import { BsVolumeUpFill } from "react-icons/bs";
import { MdLightbulbOutline } from "react-icons/md";
import SuggestedTopicsPopup from "../components/SuggestedTopicsPopup";
import TrendingTopicsPopup from "../components/TrendingTopicsPopup";
import {
  handleInput,
  handleFetchTrendingTopics,
  handleFetchSuggestedTopics,
  handleGenerateScript,
  handleGenerateVoice,
  handleGenerateVideo,
} from "../scripts/home";

// Scene Voice Card Component
const SceneVoiceCard = ({
  script,
  index,
  voiceUrl,
  imageUrl,
  isVoicePlaying,
  setIsVoicePlaying,
}) => {
  const [isCurrentPlaying, setIsCurrentPlaying] = useState(false);
  const [audioProgress, setAudioProgress] = useState(0);
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handlePlay = () => {
      setIsCurrentPlaying(true);
      setIsVoicePlaying(true);
    };

    const handlePause = () => {
      setIsCurrentPlaying(false);
      setIsVoicePlaying(false);
    };

    const handleEnded = () => {
      setIsCurrentPlaying(false);
      setIsVoicePlaying(false);
      setAudioProgress(0);
    };

    const handleTimeUpdate = () => {
      if (audio.duration) {
        const progress = (audio.currentTime / audio.duration) * 100;
        setAudioProgress(progress);
      }
    };

    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePause);
    audio.addEventListener("ended", handleEnded);
    audio.addEventListener("timeupdate", handleTimeUpdate);

    return () => {
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePause);
      audio.removeEventListener("ended", handleEnded);
      audio.removeEventListener("timeupdate", handleTimeUpdate);
    };
  }, [setIsVoicePlaying]);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (audio) {
      if (isCurrentPlaying) {
        audio.pause();
      } else {
        // Pause all other audios first
        const allAudios = document.querySelectorAll("audio");
        allAudios.forEach((a) => {
          if (a !== audio) a.pause();
        });
        audio.play();
      }
    }
  };

  return (
    <div className="flex flex-col space-y-3">
      {/* Scene Frame */}
      <div
        className={`relative aspect-[3/4] bg-zinc-800 border-2 rounded-lg overflow-hidden transition-all duration-300 ${
          isCurrentPlaying
            ? "border-blue-400 shadow-lg shadow-blue-400/20"
            : "border-zinc-600"
        }`}
      >
        {imageUrl ? (
          <img
            src={imageUrl || "/placeholder.svg"}
            alt={`Scene ${index + 1}`}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
            <div className="text-xs text-zinc-400 mb-2">Scene {index + 1}</div>
            <div className="text-sm text-zinc-300 line-clamp-4">
              {script.label}
            </div>
          </div>
        )}

        {/* Audio Progress Overlay */}
        {isCurrentPlaying && (
          <div className="absolute inset-0 bg-blue-500/10 flex items-center justify-center">
            <div className="w-16 h-16 rounded-full border-4 border-blue-400 border-t-transparent animate-spin"></div>
          </div>
        )}

        {/* Progress Bar */}
        {audioProgress > 0 && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-zinc-700">
            <div
              className="h-full bg-blue-400 transition-all duration-100"
              style={{ width: `${audioProgress}%` }}
            ></div>
          </div>
        )}

        {/* Playing Indicator */}
        {isCurrentPlaying && (
          <div className="absolute top-2 right-2">
            <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
          </div>
        )}
      </div>

      {/* Control Button (Play/Pause) */}
      <div className="flex gap-2 justify-center">
        <button
          onClick={togglePlayPause}
          disabled={isVoicePlaying && !isCurrentPlaying}
          className={`flex-1 px-3 py-2 rounded-md text-xs font-medium transition-all flex items-center justify-center gap-1 ${
            isCurrentPlaying
              ? "bg-blue-600 text-white"
              : isVoicePlaying
              ? "bg-gray-600 text-gray-400 cursor-not-allowed"
              : "bg-zinc-700 text-zinc-300 hover:bg-zinc-600"
          }`}
        >
          {isCurrentPlaying ? (
            <FiPause className="w-3 h-3" />
          ) : (
            <FiPlay className="w-3 h-3" />
          )}
          {isCurrentPlaying ? "Pause" : "Play"}
        </button>
      </div>

      {/* Hidden Audio Element */}
      <audio ref={audioRef} src={voiceUrl} />
    </div>
  );
};

const Home = () => {
  const { authFetch } = useContext(AuthContext);
  const [text, setText] = useState("");
  const textareaRef = useRef(null);
  const [trendingTopics, setTrendingTopics] = useState([]);
  const [showTrendingPopup, setShowTrendingPopup] = useState(false);
  const trendingBtnRef = useRef(null);
  const trendingPopupRef = useRef(null);
  const [isLoadingTrending, setIsLoadingTrending] = useState(false);
  const [suggestedTopics, setSuggestedTopics] = useState([]);
  const [showSuggestedPopup, setShowSuggestedPopup] = useState(false);
  const suggestedBtnRef = useRef(null);
  const popupRef = useRef(null);
  const [isLoadingSuggested, setIsLoadingSuggested] = useState(false);

  // Changed to handle array of script sections
  const [generatedScripts, setGeneratedScripts] = useState([]);
  const [showScriptArea, setShowScriptArea] = useState(false);
  const [scriptError, setScriptError] = useState(false);
  const [voiceUrl, setVoiceUrl] = useState("");
  const [isLoadingVoice, setIsLoadingVoice] = useState(false);
  const [videoId, setVideoId] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoadingVideo, setIsLoadingVideo] = useState(false);
  // New state for generated images
  const [generatedImages, setGeneratedImages] = useState([]);

  const audioRef = useRef(null);
  const [isVoicePlaying, setIsVoicePlaying] = useState(false);
  const [isLoadingScript, setIsLoadingScript] = useState(false);
  const navigate = useNavigate();

  // Auto-resize textareas
  useEffect(() => {
    const textareas = document.querySelectorAll(".script-textarea");
    textareas.forEach((textarea) => {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
    });
  }, [generatedScripts]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target) &&
        suggestedBtnRef.current &&
        !suggestedBtnRef.current.contains(event.target)
      ) {
        setShowSuggestedPopup(false);
      }
      if (
        trendingPopupRef.current &&
        !trendingPopupRef.current.contains(event.target) &&
        trendingBtnRef.current &&
        !trendingBtnRef.current.contains(event.target)
      ) {
        setShowTrendingPopup(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    const handlePlay = () => setIsVoicePlaying(true);
    const handlePauseOrEnd = () => setIsVoicePlaying(false);
    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePauseOrEnd);
    audio.addEventListener("ended", handlePauseOrEnd);
    return () => {
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePauseOrEnd);
      audio.removeEventListener("ended", handlePauseOrEnd);
    };
  }, [voiceUrl]);

  const LoadingSpinner = () => <FiLoader className="w-4 h-4 animate-spin" />;

  const handleGenerateScriptWithLoading = async () => {
    setIsLoadingScript(true);
    try {
      await handleGenerateScript(
        text,
        authFetch,
        setGeneratedScripts, // Changed to setGeneratedScripts
        setShowScriptArea,
        setScriptError,
        setVideoId
      );
    } finally {
      setIsLoadingScript(false);
    }
  };

  const handleFetchSuggestedWithLoading = async () => {
    setIsLoadingSuggested(true);
    try {
      await handleFetchSuggestedTopics(
        text,
        authFetch,
        setSuggestedTopics,
        setShowSuggestedPopup,
        setIsLoadingSuggested
      );
    } finally {
      setIsLoadingSuggested(false);
    }
  };

  const handleFetchTrendingWithLoading = async () => {
    setIsLoadingTrending(true);
    try {
      await handleFetchTrendingTopics(
        authFetch,
        setTrendingTopics,
        setShowTrendingPopup,
        setIsLoadingTrending
      );
    } finally {
      setIsLoadingTrending(false);
    }
  };

  // Handle script section updates
  const handleScriptSectionChange = (index, value) => {
    const updatedScripts = [...generatedScripts];
    updatedScripts[index] = { ...updatedScripts[index], subtitle: value };
    setGeneratedScripts(updatedScripts);
    setScriptError(value.trim() === "");
  };

  // Generate combined script text for voice generation
  const getCombinedScriptText = () => {
    return generatedScripts.map((script) => script.subtitle).join(" ");
  };

  return (
    <div className="relative flex h-screen bg-black text-white">
      <LeftSideBar />
      <div className="flex-1 flex flex-col transition-all duration-300">
        <Header />
        <div
          className={`flex-1 flex flex-col items-center justify-start px-4 overflow-y-auto relative transition-all duration-300 ${
            showScriptArea ? "pt-4" : "pt-20"
          }`}
        >
          <div
            className={`text-center mb-10 transition-all duration-300 ${
              showScriptArea ? "mt-1" : "mt-18"
            }`}
          >
            <h1 className="text-[80px] sm:text-[100px] md:text-[120px] lg:text-[150px] font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-blue-500">
              AIGen
            </h1>
            <p className="text-lg sm:text-xl md:text-2xl text-zinc-400 mt-4">
              What can I help you build?
            </p>
          </div>

          <div className="w-full max-w-3xl bg-zinc-900 rounded-xl border border-zinc-800 flex flex-col sm:flex-row justify-between items-stretch sm:items-start gap-4 p-4">
            <div className="w-full">
              <textarea
                ref={textareaRef}
                value={text}
                onInput={(e) => handleInput(e, setText, textareaRef)}
                maxLength={150}
                placeholder="Topic you want to create a script for..."
                className="w-full bg-transparent border-none outline-none resize-none text-zinc-400 placeholder:text-zinc-500 overflow-hidden"
              />
            </div>
            <div className="shrink-0">
              <button
                disabled={showScriptArea || !text.trim() || isLoadingScript}
                onClick={handleGenerateScriptWithLoading}
                className={`w-full sm:w-auto cursor-pointer text-white rounded-md px-4 py-2 flex items-center justify-center gap-2 transition-colors min-w-[60px] ${
                  showScriptArea || !text.trim() || isLoadingScript
                    ? "bg-gray-700 cursor-not-allowed"
                    : "hover:bg-gray-700"
                }`}
              >
                {isLoadingScript ? (
                  <LoadingSpinner />
                ) : (
                  <FiSend className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-3 mt-8 w-full px-2 max-w-3xl relative">
            <button
              ref={suggestedBtnRef}
              disabled={showScriptArea || isLoadingSuggested}
              onClick={handleFetchSuggestedWithLoading}
              className={`flex items-center gap-2 w-full sm:w-auto justify-center border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors min-h-[40px] ${
                showScriptArea || isLoadingSuggested
                  ? "bg-gray-700 cursor-not-allowed text-zinc-500"
                  : "bg-zinc-900 hover:bg-zinc-800 text-white"
              }`}
            >
              {isLoadingSuggested ? (
                <>
                  <LoadingSpinner />
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <MdLightbulbOutline className="w-5 h-5 text-yellow-400" />
                  <span>Suggested Topics</span>
                </>
              )}
            </button>
            <button
              ref={trendingBtnRef}
              disabled={showScriptArea || isLoadingTrending}
              onClick={handleFetchTrendingWithLoading}
              className={`flex items-center gap-2 w-full sm:w-auto justify-center border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors min-h-[40px] ${
                showScriptArea || isLoadingTrending
                  ? "bg-gray-700 cursor-not-allowed text-zinc-500"
                  : "bg-zinc-900 hover:bg-zinc-800 text-white"
              }`}
            >
              {isLoadingTrending ? (
                <>
                  <LoadingSpinner />
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <FiTrendingUp className="w-5 h-5 text-green-400" />
                  <span>Trending Topics</span>
                </>
              )}
            </button>
          </div>

          {showSuggestedPopup && (
            <SuggestedTopicsPopup
              isLoading={isLoadingSuggested}
              topics={suggestedTopics}
              onSelectTopic={(topic) => {
                setText(topic);
                setShowSuggestedPopup(false);
              }}
              anchorRef={suggestedBtnRef}
              popupRef={popupRef}
            />
          )}

          {showTrendingPopup && (
            <TrendingTopicsPopup
              isLoading={isLoadingTrending}
              topics={trendingTopics}
              onSelectTopic={(topic) => {
                setText(topic);
                setShowTrendingPopup(false);
              }}
              anchorRef={trendingBtnRef}
              popupRef={trendingPopupRef}
            />
          )}

          {showScriptArea && generatedScripts.length > 0 && (
            <div className="w-full max-w-3xl mt-6 space-y-6">
              <div className="text-zinc-400 text-lg sm:text-xl font-semibold mb-4">
                Script Sections
              </div>

              {/* Multiple Script Sections */}
              {generatedScripts.map((script, index) => (
                <div
                  key={index}
                  className="bg-zinc-900 rounded-lg border border-zinc-700 p-4 space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <div className="text-sm font-medium text-blue-400">
                      Scene {index + 1}
                    </div>
                  </div>

                  {/* Scene Description */}
                  <div className="text-sm text-zinc-300 bg-zinc-800 rounded p-3 border-l-4 border-blue-500">
                    <span className="font-medium text-zinc-200">
                      Description:{" "}
                    </span>
                    {script.label}
                  </div>

                  {/* Editable Script Content */}
                  <div>
                    <label className="text-xs text-zinc-400 mb-2 block">
                      Script Content:
                    </label>
                    <textarea
                      value={script.subtitle}
                      onChange={(e) =>
                        handleScriptSectionChange(index, e.target.value)
                      }
                      className="script-textarea w-full bg-zinc-800 text-zinc-300 border border-zinc-600 rounded-md p-3 resize-none overflow-hidden focus:border-blue-500 focus:outline-none transition-colors"
                      placeholder="Enter script content..."
                    />
                  </div>
                </div>
              ))}

              {/* Text to Speech Button - Moved to Bottom */}
              <div className="flex justify-center pt-4">
                <button
                  disabled={!!voiceUrl || isLoadingVoice}
                  onClick={() =>
                    handleGenerateVoice(
                      generatedScripts,
                      setVoiceUrl,
                      setIsLoadingVoice,
                      videoId
                    )
                  }
                  className={`text-sm font-medium text-white rounded-md px-6 py-3 transition-all flex items-center gap-2 min-w-[160px] justify-center ${
                    voiceUrl || isLoadingVoice
                      ? "bg-gray-600 cursor-not-allowed"
                      : "bg-blue-600 hover:bg-blue-700"
                  }`}
                >
                  {isLoadingVoice ? (
                    <>
                      <LoadingSpinner />
                      <span>Generating...</span>
                    </>
                  ) : (
                    "Generate Text to Speech"
                  )}
                </button>
              </div>

              {scriptError && (
                <div className="text-red-500 text-sm mt-1">
                  Script cannot be empty.
                </div>
              )}

              {voiceUrl && (
                <div className="w-full max-w-5xl mt-6 space-y-6">
                  <div className="flex items-center gap-2 text-zinc-400 sm:text-xl font-semibold text-zinc-300">
                    <span>Generated Voice Preview</span>
                    <BsVolumeUpFill
                      className={`w-5 h-5 transition-transform duration-500 ${
                        isVoicePlaying
                          ? "animate-pulse scale-110 text-blue-400"
                          : "text-zinc-500"
                      }`}
                    />
                  </div>

                  {/* Scene Voice Preview Grid - Updated to show 5 columns on XL screens */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                    {generatedScripts.map((script, index) => (
                      <SceneVoiceCard
                        key={index}
                        script={script}
                        index={index}
                        voiceUrl={voiceUrl}
                        imageUrl={generatedImages[index]} // Pass the image URL
                        isVoicePlaying={isVoicePlaying}
                        setIsVoicePlaying={setIsVoicePlaying}
                      />
                    ))}
                  </div>

                  {/* Generate Video Button */}
                  <div className="flex justify-center pt-6">
                    <button
                      disabled={!!videoUrl || isLoadingVideo}
                      onClick={() =>
                        handleGenerateVideo(
                          videoId,
                          authFetch,
                          setVideoUrl,
                          setIsLoadingVideo,
                          generatedScripts, // Pass generatedScripts
                          setGeneratedImages // Pass setGeneratedImages
                        )
                      }
                      className={`text-white text-sm font-medium px-6 py-3 rounded-md transition-all flex items-center gap-2 min-w-[160px] justify-center ${
                        videoUrl || isLoadingVideo
                          ? "bg-gray-600 cursor-not-allowed"
                          : "bg-blue-600 hover:bg-blue-700"
                      }`}
                    >
                      {isLoadingVideo ? (
                        <>
                          <LoadingSpinner />
                          <span>Generating...</span>
                        </>
                      ) : (
                        "Generate Video"
                      )}
                    </button>
                  </div>

                  <audio ref={audioRef} src={voiceUrl} />
                </div>
              )}

              {videoUrl && (
                <div className="w-full max-w-3xl mt-10">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-zinc-400 sm:text-xl font-semibold">
                      Generated video
                    </div>
                    <button
                      onClick={() =>
                        navigate("/edit-video", { state: { videoUrl } })
                      }
                      className="text-white text-sm font-medium px-3 py-1.5 rounded-md transition-all bg-blue-600 hover:bg-blue-700"
                    >
                      Edit video
                    </button>
                  </div>
                  <div className="w-full flex justify-center">
                    <video
                      src={videoUrl}
                      controls
                      className="rounded-lg border border-zinc-700 h-[300px] sm:h-[400px] md:h-[500px] lg:h-[600px] w-auto max-w-full"
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="mt-auto py-4 text-xs text-zinc-500 text-center">
            AIGen can make mistakes. Check important info.
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

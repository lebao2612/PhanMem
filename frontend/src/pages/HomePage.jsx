import { useContext, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import {
  FiSend,
  FiTrendingUp,
  FiPlay,
  FiRotateCcw,
  FiEdit,
} from "react-icons/fi";
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

  const [generatedScript, setGeneratedScript] = useState("");
  const [showScriptArea, setShowScriptArea] = useState(false);
  const [scriptError, setScriptError] = useState(false);

  const [voiceUrl, setVoiceUrl] = useState("");
  const [isLoadingVoice, setIsLoadingVoice] = useState(false);

  const [videoId, setVideoId] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoadingVideo, setIsLoadingVideo] = useState(false);

  const audioRef = useRef(null);
  const [isVoicePlaying, setIsVoicePlaying] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto"; // Reset height
      textarea.style.height = `${textarea.scrollHeight}px`; // Set to scroll height
    }
  }, [generatedScript]);

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
                disabled={showScriptArea || !text.trim()}
                onClick={() =>
                  handleGenerateScript(
                    text,
                    authFetch,
                    setGeneratedScript,
                    setShowScriptArea,
                    setScriptError,
                    setVideoId
                  )
                }
                className={`w-full sm:w-auto cursor-pointer text-white rounded-md px-4 py-2 flex items-center justify-center gap-2 transition-colors ${
                  showScriptArea || !text.trim()
                    ? "bg-gray-700 cursor-not-allowed"
                    : "hover:bg-gray-700"
                }`}
              >
                <FiSend className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-3 mt-8 w-full px-2 max-w-3xl relative">
            <button
              ref={suggestedBtnRef}
              disabled={showScriptArea}
              onClick={() =>
                handleFetchSuggestedTopics(
                  text,
                  authFetch,
                  setSuggestedTopics,
                  setShowSuggestedPopup,
                  setIsLoadingSuggested
                )
              }
              className={`flex items-center gap-2 w-full sm:w-auto justify-center border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors ${
                showScriptArea
                  ? "bg-gray-700 cursor-not-allowed text-zinc-500"
                  : "bg-zinc-900 hover:bg-zinc-800 text-white"
              }`}
            >
              <MdLightbulbOutline className="w-5 h-5 text-yellow-400" />
              <span>Suggested Topics</span>
            </button>

            <button
              ref={trendingBtnRef}
              disabled={showScriptArea}
              onClick={() =>
                handleFetchTrendingTopics(
                  authFetch,
                  setTrendingTopics,
                  setShowTrendingPopup,
                  setIsLoadingTrending
                )
              }
              className={`flex items-center gap-2 w-full sm:w-auto justify-center border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors ${
                showScriptArea
                  ? "bg-gray-700 cursor-not-allowed text-zinc-500"
                  : "bg-zinc-900 hover:bg-zinc-800 text-white"
              }`}
            >
              <FiTrendingUp className="w-5 h-5 text-green-400" />
              <span>Trending Topics</span>
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

          {showScriptArea && (
            <div className="w-full max-w-3xl mt-6 space-y-2">
              <div className="relative w-full">
                <div className="text-zinc-400 text-lg sm:text-xl font-semibold mb-2">
                  Script
                </div>
                <button
                  disabled={!!voiceUrl}
                  onClick={() =>
                    handleGenerateVoice(
                      generatedScript,
                      setVoiceUrl,
                      setIsLoadingVoice
                    )
                  }
                  className={`absolute right-0 top-0 text-sm font-medium text-white rounded-md px-3 py-1.5 transition-all ${
                    voiceUrl
                      ? "bg-gray-600 cursor-not-allowed"
                      : "bg-blue-600 hover:bg-blue-700"
                  }`}
                >
                  {isLoadingVoice ? "Loading..." : "Text to speech"}
                </button>
              </div>
              <textarea
                ref={textareaRef}
                value={generatedScript}
                onChange={(e) => {
                  const value = e.target.value;
                  setGeneratedScript(value);
                  setScriptError(value.trim() === "");
                }}
                className={`w-full bg-zinc-900 text-zinc-300 border ${
                  scriptError ? "border-red-500" : "border-zinc-700"
                } rounded-md p-4 resize-none overflow-hidden`}
                style={{ height: "auto" }}
              />

              {scriptError && (
                <div className="text-red-500 text-sm mt-1">
                  Script cannot be empty.
                </div>
              )}

              {voiceUrl && (
                <div className="w-full max-w-3xl mt-6 space-y-4">
                  <div className="flex items-center gap-2 text-zinc-400 sm:text-xl font-semibold text-zinc-300">
                    <span>Generated voice</span>
                    <BsVolumeUpFill
                      className={`w-5 h-5 transition-transform duration-500 ${
                        isVoicePlaying
                          ? "animate-pulse scale-110 text-blue-400"
                          : "text-zinc-500"
                      }`}
                    />
                  </div>

                  <div className="flex items-center justify-between flex-wrap gap-4">
                    <div className="flex gap-3">
                      <button
                        onClick={() => {
                          const audio = audioRef.current;
                          if (audio) {
                            audio.play();
                            setIsVoicePlaying(true);
                          }
                        }}
                        className="px-5 py-2 rounded-full bg-zinc-900 border border-zinc-700 hover:border-blue-500 text-sm text-white transition-all flex items-center gap-2"
                      >
                        <FiPlay className="w-4 h-4" />
                        Play voice
                      </button>

                      <button
                        onClick={() => {
                          const audio = audioRef.current;
                          if (audio) {
                            audio.currentTime = 0;
                            audio.play();
                            setIsVoicePlaying(true);
                          }
                        }}
                        className="px-5 py-2 rounded-full bg-zinc-900 border border-zinc-700 hover:border-blue-500 text-sm text-white transition-all flex items-center gap-2"
                      >
                        <FiRotateCcw className="w-4 h-4" />
                        Replay
                      </button>
                    </div>

                    <button
                      disabled={!!videoUrl}
                      onClick={() =>
                        handleGenerateVideo(
                          videoId,
                          authFetch,
                          setVideoUrl,
                          setIsLoadingVideo
                        )
                      }
                      className={`text-white text-sm font-medium px-3 py-1.5 rounded-md transition-all ${
                        videoUrl
                          ? "bg-gray-600 cursor-not-allowed"
                          : "bg-blue-600 hover:bg-blue-700"
                      }`}
                    >
                      {isLoadingVideo ? "Generating..." : "Generate video"}
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

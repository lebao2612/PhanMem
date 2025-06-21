import { useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import { FiSend, FiTrendingUp } from "react-icons/fi";
import { MdLightbulbOutline } from "react-icons/md";
import SuggestedTopicsPopup from "../components/SuggestedTopicsPopup";
import TrendingTopicsPopup from "../components/TrendingTopicsPopup";
import {
  handleInput,
  handleFetchTrendingTopics,
  handleFetchSuggestedTopics,
  handleGenerateScript,
  handleGenerateVoice,
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

  const [videoId, setVideoId] = useState(""); // ✅ dùng state để lưu ID thật

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
          {/* Title */}
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

          {/* Text Input */}
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
                onClick={() =>
                  handleGenerateScript(
                    text,
                    authFetch,
                    setGeneratedScript,
                    setShowScriptArea,
                    setScriptError,
                    setVideoId // ✅ truyền vào để lưu ID
                  )
                }
                className="w-full sm:w-auto hover:bg-gray-700 cursor-pointer text-white rounded-md px-4 py-2 flex items-center justify-center gap-2 transition-colors"
              >
                <FiSend className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap justify-center gap-3 mt-8 w-full px-2 max-w-3xl relative">
            <button
              ref={suggestedBtnRef}
              onClick={() =>
                handleFetchSuggestedTopics(
                  text,
                  authFetch,
                  setSuggestedTopics,
                  setShowSuggestedPopup,
                  setIsLoadingSuggested
                )
              }
              className="flex items-center gap-2 w-full sm:w-auto justify-center bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors"
            >
              <MdLightbulbOutline className="w-5 h-5 text-yellow-400" />
              <span>Suggested Topics</span>
            </button>

            <button
              ref={trendingBtnRef}
              onClick={() =>
                handleFetchTrendingTopics(
                  authFetch,
                  setTrendingTopics,
                  setShowTrendingPopup,
                  setIsLoadingTrending
                )
              }
              className="relative flex items-center gap-2 w-full sm:w-auto justify-center bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-full px-4 py-2 text-sm transition-colors"
            >
              <FiTrendingUp className="w-5 h-5 text-green-400" />
              <span>Trending Topics</span>
            </button>
          </div>

          {/* Popups */}
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

          {/* Generated Script */}
          {showScriptArea && (
            <div className="w-full max-w-3xl mt-6 space-y-2">
              <div className="relative w-full">
                <div className="text-zinc-400 text-lg sm:text-xl font-semibold mb-2">
                  Script
                </div>
                <button
                  onClick={() =>
                    handleGenerateVoice(
                      videoId,
                      authFetch,
                      setVoiceUrl,
                      setIsLoadingVoice
                    )
                  }
                  className="absolute right-0 top-0 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md px-3 py-1.5 transition-all"
                >
                  {isLoadingVoice ? "Loading..." : "Text to speak"}
                </button>
              </div>
              <textarea
                value={generatedScript}
                onChange={(e) => {
                  const value = e.target.value;
                  setGeneratedScript(value);
                  setScriptError(value.trim() === "");
                }}
                className={`w-full bg-zinc-900 text-zinc-300 border ${
                  scriptError ? "border-red-500" : "border-zinc-700"
                } rounded-md p-4 resize-none`}
                rows={Math.max(5, generatedScript.split("\n").length)}
              />
              {scriptError && (
                <div className="text-red-500 text-sm mt-1">
                  Script cannot be empty.
                </div>
              )}

              {/* Audio Player */}
              {voiceUrl && (
                <div className="mt-4">
                  <audio controls className="w-full">
                    <source src={voiceUrl} type="audio/mpeg" />
                    Your browser does not support the audio element.
                  </audio>
                </div>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="mt-auto py-4 text-xs text-zinc-500 text-center">
            AIGen can make mistakes. Check important info.
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

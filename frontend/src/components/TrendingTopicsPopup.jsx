import React from "react";

const TrendingTopicsPopup = ({
  isLoading,
  topics,
  onSelectTopic,
  anchorRef,
  popupRef,
}) => {
  const anchorRect = anchorRef.current?.getBoundingClientRect();

  return (
    <div
      ref={popupRef}
      className="fixed z-50 bg-zinc-800 text-sm text-zinc-200 border border-zinc-700 rounded-md shadow-lg p-3"
      style={{
        bottom: `calc(100vh - ${anchorRect?.bottom}px)`,
        left: anchorRect?.right + 10,
      }}
    >
      {isLoading ? (
        <div className="text-zinc-400 italic">Loading...</div>
      ) : topics.length > 0 ? (
        <ul className="flex flex-col gap-y-1 max-w-[300px]">
          {topics.map((topic, index) => (
            <li
              key={index}
              onClick={() => onSelectTopic(topic)}
              className="cursor-pointer hover:bg-zinc-700 px-2 py-1 rounded-md transition-colors"
            >
              {topic}
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-zinc-400 italic">No trending topics.</div>
      )}
    </div>
  );
};

export default TrendingTopicsPopup;

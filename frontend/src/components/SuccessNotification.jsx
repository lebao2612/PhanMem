"use client";

import { useEffect } from "react";
import { CheckCircle, X, AlertCircle } from "lucide-react";

const Notification = ({
  message,
  onClose,
  duration = 3000,
  type = "success",
}) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [onClose, duration]);

  const isSuccess = type === "success";
  const bgColor = isSuccess ? "bg-green-600" : "bg-red-600";
  const textColor = isSuccess ? "text-green-200" : "text-red-200";
  const iconColor = isSuccess ? "text-green-200" : "text-red-200";
  const hoverColor = isSuccess ? "hover:bg-green-700" : "hover:bg-red-700";

  return (
    <div className="fixed top-4 right-4 z-50 animate-slide-in">
      <div
        className={`${bgColor} text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 min-w-[300px]`}
      >
        <div className="flex-shrink-0">
          {isSuccess ? (
            <CheckCircle className={`w-6 h-6 ${iconColor}`} />
          ) : (
            <AlertCircle className={`w-6 h-6 ${iconColor}`} />
          )}
        </div>
        <div className="flex-1">
          <p className="font-medium">{isSuccess ? "Success!" : "Error!"}</p>
          <p className={`text-sm ${textColor}`}>{message}</p>
        </div>
        <button
          onClick={onClose}
          className={`${textColor} hover:text-white transition-colors`}
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default Notification;

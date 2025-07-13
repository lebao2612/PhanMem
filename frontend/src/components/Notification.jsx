"use client";

import { useEffect } from "react";
import { CheckCircle, XCircle, X } from "lucide-react";

const Notification = ({ message, type, onClose, renderActionButton }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000); // Tự động đóng sau 5 giây

    return () => clearTimeout(timer);
  }, [onClose]);

  const bgColor = type === "success" ? "bg-green-600" : "bg-red-600";
  const Icon = type === "success" ? CheckCircle : XCircle;

  return (
    <div
      // Các lớp này đảm bảo căn giữa chính xác trong viewport
      className={`fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-6 rounded-lg shadow-2xl text-white flex flex-col items-center space-y-4 animate-fade-in-scale ${bgColor} z-50 min-w-[300px] max-w-sm text-center`}
    >
      <Icon className="w-10 h-10" />
      <div className="flex flex-col items-center">
        <p className="font-bold text-lg">{message}</p>
        {renderActionButton && (
          <div className="mt-4">{renderActionButton()}</div>
        )}
      </div>
      <button
        onClick={onClose}
        className="absolute top-2 right-2 text-white/80 hover:text-white"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
};

export default Notification;

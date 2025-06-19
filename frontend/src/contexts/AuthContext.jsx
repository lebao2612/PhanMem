import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const stored = sessionStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const authFetch = async (url, options = {}) => {
    const token = sessionStorage.getItem("token");
    console.log("Token:", token);
    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };

    const res = await fetch(url, {
      ...options,
      headers
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData?.error || "Lỗi server");
    }

    return res.json();
  };

  return (
    <AuthContext.Provider value={{ user, setUser, authFetch }}>
      {children}
    </AuthContext.Provider>
  );
};

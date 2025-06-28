import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const stored = sessionStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const authFetch = async (url, options = {}) => {
    const token = sessionStorage.getItem("token");
    if (!token) {
      throw new Error("Chưa đăng nhập hoặc token không tồn tại");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };

    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    let res;
    try {
      res = await fetch(url, {
        ...options,
        headers,
      });
    } catch (err) {
      throw new Error("Không thể kết nối đến server");
    }

    // Xử lý 204 No Content
    if (res.status === 204) return null;

    const {success, data, error} = await res.json();
    if (!res.ok || !success) {
      if (res.status === 401) {
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("user");
        setUser(null);
        throw new Error("Phiên đăng nhập đã hết hạn");
      }

      throw new Error(error?.message || `Lỗi hệ thống (${res.status})`);
    }

    return data;
  };

  return (
    <AuthContext.Provider value={{ user, setUser, authFetch }}>
      {children}
    </AuthContext.Provider>
  );
};

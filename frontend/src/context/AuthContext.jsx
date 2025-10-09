// src/context/AuthContext.jsx
import { createContext, useState } from "react";
import {jwtDecode} from "jwt-decode";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [role, setRole] = useState(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) return null;
    const decoded = jwtDecode(storedToken);
    return decoded.role;
  });

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    const decoded = jwtDecode(newToken);
    setRole(decoded.role);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

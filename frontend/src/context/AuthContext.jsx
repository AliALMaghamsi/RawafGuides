import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [role, setRole] = useState(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) return null;
    try {
      const decoded = jwtDecode(storedToken);
      return decoded.role;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true); 

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    try {
      const decoded = jwtDecode(newToken);
      setRole(decoded.role);
    } catch {
      setRole(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setRole(null);
  };

  // ✅ Check token expiration on page load / refresh
  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const now = Date.now() / 1000;
        if (decoded.exp < now) {
          logout(); // token expired
        } else {
          setRole(decoded.role);
        }
      } catch {
        logout();
      }
    }
    setLoading(false); // done checking
  }, [token]);

  return (
    <AuthContext.Provider value={{ token, role, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

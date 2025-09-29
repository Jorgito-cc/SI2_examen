import { createContext, useContext, useEffect, useState } from "react";
import { loginRequest, meRequest } from "../api";

const AuthCtx = createContext(null);

// Mapeo: si is_staff o tiene rol "ADMINISTRADOR" => "ADMIN"
function computeRoleFromUser(me) {
  const names = (me?.roles || []).map(r => (r?.nombre || r || "").toUpperCase());
  const isAdmin = me?.is_staff || names.includes("ADMINISTRADOR");
  if (isAdmin) return "ADMINISTRADOR";
  return names[0] || null; // GUARDIA, PERSONAL, PROPIETARIO, INQUILINO...
}

export default function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // null=cargando
  const [role, setRole] = useState(null);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("access") || null);

  // Autocargar sesión si hay token guardado
  useEffect(() => {
    (async () => {
      if (!token) { setIsAuthenticated(false); setUser(null); setRole(null); return; }
      try {
        const me = await meRequest(token);
        setUser(me);
        setRole(computeRoleFromUser(me));
        setIsAuthenticated(true);
      } catch {
        // token inválido
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        setToken(null);
        setIsAuthenticated(false);
        setUser(null);
        setRole(null);
      }
    })();
  }, [token]);

  // API del contexto
  const login = async ({ username, password, remember }) => {
    const payload = await loginRequest({ username, password });
    const access = payload.access;
    localStorage.setItem("access", access);
    if (payload.refresh) localStorage.setItem("refresh", payload.refresh);
    if (remember) localStorage.setItem("remember_username", username);
    else localStorage.removeItem("remember_username");
    setToken(access); // dispara el useEffect y cargará /me
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setToken(null);
    setIsAuthenticated(false);
    setUser(null);
    setRole(null);
  };

  return (
    <AuthCtx.Provider value={{ isAuthenticated, role, user, token, login, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}

export const useAuth = () => useContext(AuthCtx);
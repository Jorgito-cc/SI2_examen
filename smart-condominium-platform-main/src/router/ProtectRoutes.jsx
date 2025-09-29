// src/routes/ProtectedRoute.jsx
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContex";

export default function ProtectedRoutes({ children, allowedRoles }) {
  const { isAuthenticated, role } = useAuth();
  const location = useLocation();

  if (isAuthenticated === null) {
    return <div style={{ padding: 24 }}>Cargando…</div>; // Spinner si quieres
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (Array.isArray(allowedRoles) && allowedRoles.length > 0) {
    if (!role || !allowedRoles.map(r => r.toUpperCase()).includes(String(role).toUpperCase())) {
      return <Navigate to="/" replace />;
    }
  }

  return children;
}
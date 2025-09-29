import axios from "axios";

// Lee la URL desde tu .env (ejemplo con Vite: VITE_API_URL)
export const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const instance = axios.create({
  baseURL: BASE_URL,
});

// Interceptor: agrega token automáticamente si existe
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default instance;

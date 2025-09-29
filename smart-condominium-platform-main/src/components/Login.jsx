import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import "../styles/login.css";
import { getHttpErrorMessage } from "../utils/httpErrors";
import { useAuth } from "../context/AuthContex";
import { useLocation, useNavigate } from "react-router-dom";

export const Login = ({ onSwitchRegister, modal = true, onClose }) => {
  const [showPwd, setShowPwd] = useState(false);
  const { login, isAuthenticated, role } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const { register, handleSubmit, formState:{ errors, isSubmitting }, setError, setValue } = useForm({
    mode: "onTouched",
    defaultValues: { username: "", password: "", remember: true },
  });

  useEffect(() => {
    const remembered = localStorage.getItem("remember_username");
    if (remembered) { setValue("username", remembered); setValue("remember", true); }
  }, [setValue]);

  // si ya está logueado, redirige
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname;
      if (from) return navigate(from, { replace: true });
      if (role === "ADMINISTRADOR") return navigate("/admin", { replace: true });
      if (role === "GUARDIA") return navigate("/guardia", { replace: true });
      navigate("/", { replace: true });
    }
  }, [isAuthenticated, role, navigate, location.state]);

  const submit = async (data) => {
    try {
      await login({ username: data.username, password: data.password, remember: data.remember });
      toast.success("¡Bienvenido! Sesión iniciada.");
    } catch (err) {
      toast.error(getHttpErrorMessage(err));
      setError("root", { message: err?.message || "Error al iniciar sesión" });
    }
  };

  return (
    <div className={`login ${modal ? "login--modal" : ""}`} role="dialog" aria-modal="true">
      <div className="login__card">
        <button className="login__close" aria-label="Cerrar" onClick={onClose}>×</button>

        <div className="login__brand">
          <svg viewBox="0 0 24 24" width="36" height="36" fill="#2563eb">
            <path d="M12 3 2 10v11h7v-6h6v6h7V10z" />
          </svg>
          <h2 className="login__title">Iniciar sesión</h2>
          <p className="login__subtitle">Smart Condominios</p>
        </div>

        <form onSubmit={handleSubmit(submit)} className="login__form">
          <label className="login__label">Usuario</label>
          <input
            type="text"
            placeholder="Tu usuario"
            className={`login__input ${errors.username ? "login__input--error" : ""}`}
            {...register("username", { required: "Usuario requerido", minLength: { value: 3, message: "Mínimo 3 caracteres" }})}
          />
          {errors.username && <span className="login__error">{errors.username.message}</span>}

          <label className="login__label">Contraseña</label>
          <div className="login__password">
            <input
              type={showPwd ? "text" : "password"}
              placeholder="••••••••"
              className={`login__input ${errors.password ? "login__input--error" : ""}`}
              {...register("password", { required: "Contraseña requerida", minLength: { value: 6, message: "Mínimo 6 caracteres" }})}
            />
            <button type="button" className="login__toggle" onClick={() => setShowPwd(!showPwd)}>
              {showPwd ? "Ocultar" : "Mostrar"}
            </button>
          </div>
          {errors.password && <span className="login__error">{errors.password.message}</span>}

          <div className="login__row">
            <label className="login__checkbox">
              <input type="checkbox" {...register("remember")} /> Recordarme
            </label>
            <a className="login__link" href="/forgot">¿Olvidaste contra?</a>
          </div>

          {errors.root?.message && <div className="login__error">{errors.root.message}</div>}

          <button className="btn btn--primary" disabled={isSubmitting}>Ingresar</button>
          <button type="button" className="btn btn--ghost" onClick={onSwitchRegister}>Crear cuenta</button>

          <div className="login__divider"><span>o continúa con</span></div>
          <div className="login__providers">
            <button type="button" className="login__provider">Google</button>
            <button type="button" className="login__provider">GitHub</button>
          </div>
        </form>
      </div>
    </div>
  );
};
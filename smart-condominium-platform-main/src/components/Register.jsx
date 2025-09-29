// src/components/Register/Register.jsx
import "../styles/register.css";
import { useForm } from "react-hook-form";
import { useState } from "react";

export const Register = ({ modal = true, onClose, onSwitchLogin }) => {
  const [showPwd, setShowPwd] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm({
    mode: "onTouched",
    defaultValues: {
      name: "",
      password: "",
    },
  });

  const submit = async (data) => {
    try {
      // Aquí conectas tu API real
      console.log("Registro:", data);
      alert("Registro exitoso (demo)");
    } catch (err) {
      setError("root", {
        message: err?.message || "No se pudo registrar.",
      });
    }
  };

  return (
    <div
      className={`register ${modal ? "register--modal" : ""}`}
      role="dialog"
      aria-modal="true"
    >
      <button className="register__close" aria-label="Cerrar" onClick={onClose}>
        ×
      </button>

      <div className="register__card">
        <div className="register__brand">
          <svg viewBox="0 0 24 24" width="36" height="36" fill="#2563eb">
            <path d="M12 3 2 10v11h7v-6h6v6h7V10z" />
          </svg>
          <div>
            <h2 className="register__title">Crear cuenta</h2>
            <p className="register__subtitle">Smart Condominios</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(submit)} className="register__form">
          {/* Nombre */}
          <label className="register__label">Nombre</label>
          <input
            type="text"
            placeholder="Tu nombre"
            className={`register__input ${errors.name ? "register__input--error" : ""}`}
            {...register("name", {
              required: "Nombre requerido",
              minLength: { value: 3, message: "Mínimo 3 caracteres" },
            })}
          />
          {errors.name && <span className="register__error">{errors.name.message}</span>}

          {/* Contraseña */}
          <label className="register__label">Contraseña</label>
          <div className="register__password">
            <input
              type={showPwd ? "text" : "password"}
              placeholder="••••••••"
              className={`register__input ${errors.password ? "register__input--error" : ""}`}
              {...register("password", {
                required: "Contraseña requerida",
                minLength: { value: 6, message: "Mínimo 6 caracteres" },
              })}
            />
            <button
              type="button"
              className="register__toggle"
              onClick={() => setShowPwd(!showPwd)}
              aria-label={showPwd ? "Ocultar contraseña" : "Mostrar contraseña"}
            >
              {showPwd ? "Ocultar" : "Mostrar"}
            </button>
          </div>
          {errors.password && <span className="register__error">{errors.password.message}</span>}

          {/* Términos */}
          <p className="register__terms">
            Al crear una cuenta, aceptas nuestros{" "}
            <a href="#">Términos de servicio</a> y{" "}
            <a href="#">Política de privacidad</a>.
          </p>

          {/* Error general */}
          {errors.root?.message && (
            <div className="register__error">{errors.root.message}</div>
          )}

          {/* Acciones */}
          <button className="btn btn--primary" disabled={isSubmitting}>
            {isSubmitting ? "Registrando..." : "Registrarse"}
          </button>

          {/* Botón para volver a login */}
          <button
            type="button"
            className="btn btn--ghost"
            onClick={onSwitchLogin}
          >
            ¿Ya tienes cuenta? Inicia sesión
          </button>

          {/* Divider y providers */}
          <div className="register__divider"><span>o continúa con</span></div>
          <div className="register__providers">
            <button className="register__provider">Google</button>
            <button className="register__provider">GitHub</button>
          </div>
        </form>
      </div>
    </div>
  );
};

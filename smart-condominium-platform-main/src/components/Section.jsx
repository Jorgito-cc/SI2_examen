import { useState } from "react";
import "../styles/section.css";
import { Login } from "./Login";
import { Register } from "./Register";

export default function Section() {
  const [authModal, setAuthModal] = useState(null);
  const openLogin = () => setAuthModal("login");
  const openRegister = () => setAuthModal("register");
  const closeModal = () => setAuthModal(null);
  return (
    <section className="section" id="inicio" aria-labelledby="section-title">
      <div className="section__container">
        {/* Columna izquierda: texto + CTAs */}
        <div className="section__content">
          <h1 className="section__title" id="section-title">
            Administración Inteligente de <br /> Condominios
          </h1>

          <p className="section__subtitle">
            Finanzas, Reservas y Seguridad con Inteligencia Artificial
          </p>

          <div className="section__ctas">
            <a href="#demo_movil" className="btn btn--primary">
              Probar Demo
            </a>
         <button className="btn btn--ghost" onClick={openLogin}>

              Iniciar Sesión
            </button>
          </div>
        </div>
        {/* Renderiza el modal correspondiente */}
        {authModal === "login" && (
          <Login
            modal
            onClose={closeModal}
            onSwitchRegister={openRegister} // 👈 Cuando hace clic en "Crear cuenta"
          />
        )}
        {authModal === "register" && (
          <Register
            modal
            onClose={closeModal}
            onSwitchLogin={openLogin} // 👈 Si quieres botón "¿Ya tienes cuenta?"
          />
        )}

        {/* Columna derecha: mockups ilustrativos (monitor + móvil) */}
        <div className="section__media" aria-hidden="true">
          {/* Monitor */}
          <div className="mock monitor">
            <div className="monitor__kpis">
              <span className="chip">8,5%</span>
              <span className="chip">5</span>
              <span className="chip">12</span>
            </div>
            <div className="monitor__table">
              <span className="bar bar--w70" />
              <span className="bar bar--w40" />
              <span className="bar bar--w55" />
              <span className="bar bar--w30" />
            </div>
            <div className="monitor__stand" />
          </div>

          {/* Móvil */}
          <div className="mock phone">
            <div className="phone__row">
              <span className="dot" />
              <span className="line line--w60" />
              <span className="tag">35 (m)</span>
            </div>
            <div className="phone__row">
              <span className="dot" />
              <span className="line line--w45" />
              <span className="tag tag--muted">15 (m)</span>
            </div>
            <div className="phone__footer">
              <span className="pill">Seguridad</span>
              <span className="cta">Pagar</span>
            </div>
          </div>
        </div>
      </div>

      {/* Franja de features */}
      <div
        className="section__features"
        id="funcionalidades"
        aria-label="Características"
      >
        <div className="section__feature">
          <div className="section__feature-icon" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <rect
                x="3"
                y="6"
                width="18"
                height="12"
                rx="3"
                stroke="#2563eb"
                strokeWidth="2"
              />
              <rect
                x="5.5"
                y="10"
                width="6"
                height="2.5"
                fill="#2563eb"
                opacity=".2"
              />
            </svg>
          </div>
          <h3 className="section__feature-title">Finanzas</h3>
          <p className="section__feature-text">
            Pagos en línea, gestión de morosidad
          </p>
        </div>

        <div className="section__feature">
          <div className="section__feature-icon" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <rect
                x="3"
                y="5"
                width="18"
                height="16"
                rx="3"
                stroke="#2563eb"
                strokeWidth="2"
              />
              <path d="M3 9h18" stroke="#2563eb" strokeWidth="2" />
              <rect
                x="7"
                y="12"
                width="4"
                height="3"
                fill="#2563eb"
                opacity=".2"
              />
            </svg>
          </div>
          <h3 className="section__feature-title">Reservas</h3>
          <p className="section__feature-text">Áreas comunes y eventos</p>
        </div>

        <div className="section__feature">
          <div className="section__feature-icon" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6l7-3z"
                stroke="#2563eb"
                strokeWidth="2"
              />
              <circle cx="12" cy="12" r="3" fill="#2563eb" opacity=".25" />
            </svg>
          </div>
          <h3 className="section__feature-title">Seguridad IA</h3>
          <p className="section__feature-text">Reconocimiento facial y OCR</p>
        </div>
      </div>
    </section>
  );
}

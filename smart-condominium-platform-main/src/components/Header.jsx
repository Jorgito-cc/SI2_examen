import React, { useEffect, useState } from "react";
import "../styles/header.css";

export const Header = () => {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`header ${scrolled ? "header--scrolled" : ""}`}>
      {/* CONTENEDOR SUPERIOR */}
      <div className="header__container">
        {/* Brand */}
        <a href="#" className="header__brand" aria-label="Smart Condo - Inicio">
          <span className="header__logo" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
              <path d="M12 3 2 10v11h7v-6h6v6h7V10z" />
            </svg>
          </span>
          <span className="header__title">Smart Condominios</span>
        </a>

        {/* Navegación (desktop) */}
        <nav className="header__nav" aria-label="principal">
          <a href="#inicio" className="header__link header__link--active">Inicio</a>
          <a href="#funcionalidades" className="header__link">Funcionalidades</a>
          <a href="#demo_movil" className="header__link">Demo Móvil</a>
        </nav>

        {/* Acciones (buscador / menú móvil) */}
        <div className="header__actions">
          {/* (opcional) botón de búsqueda aquí */}
          <button
            className={`header__burger ${open ? "header__burger--active" : ""}`}
            aria-label="Abrir menú"
            aria-expanded={open}
            aria-controls="menu-movil"
            onClick={() => setOpen(v => !v)}
          >
            <span className="header__burger-line" />
            <span className="header__burger-line" />
            <span className="header__burger-line" />
          </button>
        </div>
      </div>

      {/* MENÚ MÓVIL (fuera del container) */}
      <div
        id="menu-movil"
        className={`header__menu ${open ? "header__menu--open" : ""}`}
        hidden={!open}                    // mejora accesibilidad
      >
        <a className="header__menu-link" href="#inicio" onClick={() => setOpen(false)}>Inicio</a>
        <a className="header__menu-link" href="#funcionalidades" onClick={() => setOpen(false)}>Funcionalidades</a>
        <a className="header__menu-link" href="#demo_movil" onClick={() => setOpen(false)}>Demo</a>
        <a className="header__menu-link" href="#contacto" onClick={() => setOpen(false)}>Contacto</a>

        <div className="header__menu-cta">
          <a className="btn btn--primary" href="#demo_movil" onClick={() => setOpen(false)}>Probar demo</a>
          <a className="btn btn--ghost" href="/login" onClick={() => setOpen(false)}>Iniciar sesión</a>
        </div>
      </div>
    </header>
  );
};

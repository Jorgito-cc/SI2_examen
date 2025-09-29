import "./../styles/footer.css";

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer" id="contacto" aria-labelledby="footer-title">
      <div className="footer__container">
        {/* Brand */}
        <div className="footer__brand">
          <span className="footer__logo" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M12 3 2 10v11h7v-6h6v6h7V10z" />
            </svg>
          </span>
          <div>
            <h2 className="footer__title" id="footer-title">Smart Condo</h2>
            <p className="footer__desc">
              Plataforma web y móvil para administración de condominios con IA
              (finanzas, reservas y seguridad).
            </p>
          </div>
        </div>

        {/* Columns */}
        <div className="footer__grid" role="navigation" aria-label="Enlaces de pie">
          <div className="footer__col">
            <h3 className="footer__heading">Producto</h3>
            <ul className="footer__list">
              <li><a className="footer__link" href="#inicio">Inicio</a></li>
              <li><a className="footer__link" href="#funcionalidades">Funcionalidades</a></li>
              <li><a className="footer__link" href="#demo_movil">Demo móvil</a></li>
            </ul>
          </div>

          <div className="footer__col">
            <h3 className="footer__heading">Recursos</h3>
            <ul className="footer__list">
              <li>
                <a className="footer__link" href="https://github.com/usuario/smart-condo-platform"
                   target="_blank" rel="noreferrer">
                  GitHub
                </a>
              </li>
              <li><a className="footer__link" href="/docs">Documentación</a></li>
              <li><a className="footer__link" href="/privacy">Privacidad</a></li>
            </ul>
          </div>

          <div className="footer__col">
            <h3 className="footer__heading">Contacto</h3>
            <ul className="footer__list">
              <li><a className="footer__link" href="mailto:contacto@smartcondo.dev">contacto@smartcondo.dev</a></li>
              <li><span className="footer__text">UAGRM – FICCT</span></li>
            </ul>
            <div className="footer__social" aria-label="Redes sociales">
              <a className="footer__social-btn" href="https://github.com/" target="_blank" rel="noreferrer" aria-label="GitHub">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.4-4-1.4-.5-1.2-1.2-1.5-1.2-1.5-1-.7.1-.7.1-.7 1.1.1 1.7 1.1 1.7 1.1 1 .1.9-.8 1.8-1.2-2.7-.3-5.6-1.4-5.6-6.2 0-1.3.5-2.5 1.2-3.4-.1-.3-.6-1.6.1-3.4 0 0 1.1-.4 3.6 1.3a12.5 12.5 0 0 1 6.6 0c2.5-1.7 3.6-1.3 3.6-1.3.7 1.8.2 3.1.1 3.4.8.9 1.2 2.1 1.2 3.4 0 4.8-2.9 5.9-5.6 6.2.9.8 1 1.6 1 2.6v3.8c0 .3.2.7.8.6A12 12 0 0 0 12 .5z"/></svg>
              </a>
              <a className="footer__social-btn" href="https://twitter.com/" target="_blank" rel="noreferrer" aria-label="Twitter/X">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.1 3H16l-4 6.4L7.9 3H3.5l6.3 9.3L3 21h4.1l4.6-7 4.6 7H20L13.8 12.1 20.1 3z"/></svg>
              </a>
              <a className="footer__social-btn" href="https://instagram.com/" target="_blank" rel="noreferrer" aria-label="Instagram">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.9.2 2.3.4.6.2 1 .5 1.5.9.4.4.7.9.9 1.5.2.4.3 1.1.4 2.3.1 1.2.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.9-.4 2.3-.2.6-.5 1-1 1.5-.4.4-.9.7-1.5.9-.4.2-1.1.3-2.3.4-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.9-.2-2.3-.4a3.7 3.7 0 0 1-1.5-.9 3.7 3.7 0 0 1-.9-1.5c-.2-.4-.3-1.1-.4-2.3C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.9.4-2.3.2-.6.5-1 1-1.5.4-.4.9-.7 1.5-.9.4-.2 1.1-.3 2.3-.4C8.4 2.2 8.8 2.2 12 2.2m0 1.8c-3.1 0-3.5 0-4.7.1-1 .1-1.5.2-1.9.3-.5.2-.8.4-1.2.8-.4.4-.6.7-.8 1.2-.1.4-.3.9-.3 1.9-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c.1 1 .2 1.5.3 1.9.2.5.4.8.8 1.2.4.4.7.6 1.2.8.4.1.9.3 1.9.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1-.1 1.5-.2 1.9-.3.5-.2.8-.4 1.2-.8.4-.4.6-.7.8-1.2.1-.4.3-.9.3-1.9.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1-.2-1.5-.3-1.9a2.8 2.8 0 0 0-.8-1.2c-.4-.4-.7-.6-1.2-.8-.4-.1-.9-.3-1.9-.3-1.2-.1-1.6-.1-4.7-.1zM12 5.8a6.2 6.2 0 1 1 0 12.4 6.2 6.2 0 0 1 0-12.4zm0 2a4.2 4.2 0 1 0 0 8.4 4.2 4.2 0 0 0 0-8.4z"/></svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom */}
      <div className="footer__bottom">
        <div className="footer__legal">© {year} Smart Condo</div>
        <div className="footer__smalllinks">
          <a className="footer__smalllink" href="/terms">Términos</a>
          <a className="footer__smalllink" href="/privacy">Privacidad</a>
        </div>
      </div>
    </footer>
  );
}

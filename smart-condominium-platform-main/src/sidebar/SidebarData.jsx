// sidebarData.jsx
import {
  FaUserShield,
  FaUsers,
  FaUserTie,
  FaHome,
  FaQrcode,
  FaCar,
  FaBullhorn,
  FaWarehouse,
  FaClipboardList,
  FaMoneyBillWave,
  FaFileInvoiceDollar,
  FaCashRegister,
  FaRobot,
  FaCamera,
  FaExclamationTriangle,
  FaTools,
  FaChartBar,
  FaComments,
  FaBookOpen,
  FaBell,
  FaCogs,
} from "react-icons/fa";

/**
 * Menú pensado para ADMIN WEB en base a tus CUs:
 * - Autenticación (gestión desde admin si la necesitas)
 * - Usuarios & Roles, Unidades, Integrantes, Personal
 * - Visitas & QR, Vehículos, Bitácora
 * - Comunicación/Avisos, Notificaciones (plantillas/envíos)
 * - Áreas Comunes (config), Reservas (vista admin)
 * - Finanzas: Tarifas, Facturación, Pagos/Conciliación
 * - Seguridad IA: Facial, LPR/OCR, Anomalías
 * - Mantenimiento
 * - Reportes & Analítica
 * - Feedback/Sugerencias
 * //scscasvbgb
 * 
 */

export const BRAND = "SmartCondo.Admin";

export const sections = [
  {
    key: "usuarios",
    icon: <FaUsers />,
    title: "Usuarios",
    items: [
      { label: "Lista de Usuarios", to: "/admin/usuarios" },              // CU4
      { label: "Gestionar Personal", to: "/admin/personalPage" },             // CU7
            { label: "registrar Personal", to: "/admin/registrarpersonal" },             // CU7

      { label: "cu5", to: "/admin/" },                     // CU5
    ],
  },
  {
    key: "unidades",
    icon: <FaHome />,
    title: "Unidades",
    items: [
      { label: "Unidades Habitacionales", to: "/admin/unidadpage" },        // CU6
            { label: "Registrar Unidades Habitacionales", to: "/admin/registrarunidades" },        // CU6asdqefwfaasd

      { label: "Integrantes de Unidad", to: "/admin/residentespages" },       // CU9
            { label: "Registrar Integrantes de Unidad", to: "/admin/registrarresidentes" },       // CU9

    ],
  },
  {
    key: "accesos",
    icon: <FaQrcode />,
    title: "Accesos",
    items: [
      { label: "Visitas & QR", to: "/admin/visitas" },                    // CU10
      { label: "Vehículos de Residentes", to: "/admin/vehiculos" },       // CU11
      { label: "Bitacora", to: "/admin/bitacoraPage" },               // CU8
    ],
  },
  {
    key: "comunicacion",
    icon: <FaBullhorn />,
    title: "Comunicación",
    items: [
      { label: "Avisos/Comunicados", to: "/admin/avisos" },               // CU14
      { label: "Notificaciones Push", to: "/admin/notificaciones" },      // CU24 (motor/plantillas)
    ],
  },
  {
    key: "areas",
    icon: <FaWarehouse />,
    title: "Áreas Comunes",
    items: [
      { label: "Configurar Áreas", to: "/admin/areas" },                  // CU23 (configuración)
      { label: "Reservas (admin)", to: "/admin/reservas" },               // CU15 (vista admin)
    ],
  },
  {
    key: "finanzas",
    icon: <FaMoneyBillWave />,
    title: "Finanzas",
    items: [
      { label: "Tarifas (Expensas/Multas)", to: "/admin/tarifas" },       // CU16
      { label: "Facturación", to: "/admin/facturacion" },                 // CU25 (Facturación periódica)
      { label: "Pagos & Conciliación", to: "/admin/conciliacion" },       // CU19/CU20
    ],
  },
  {
    key: "seguridadIA",
    icon: <FaRobot />,
    title: "Seguridad IA",
    items: [
      { label: "Reconocimiento Facial", to: "/admin/seguridad/facial" },  // CU20
      { label: "LPR/OCR Vehicular", to: "/admin/seguridad/lpr" },         // CU19
      { label: "Detección de Anomalías", to: "/admin/seguridad/anomalias" }, // CU17
      { label: "Reportes de Incidente", to: "/admin/incidentes" },        // CU18
    ],
  },
  {
    key: "mantenimiento",
    icon: <FaTools />,
    title: "Mantenimiento",
    items: [
      { label: "Activos & OT", to: "/admin/mantenimiento" },              // CU21
    ],
  },
  {
    key: "reportes",
    icon: <FaChartBar />,
    title: "Reportes",
    items: [
      { label: "Reportes & Analítica", to: "/admin/reportes" },           // CU22
    ],
  },
  {
    key: "feedback",
    icon: <FaComments />,
    title: "Feedback",
    items: [
      { label: "Sugerencias", to: "/admin/feedback" },                    // CU24
    ],
  },
];

export const soporteLink = { label: "Soporte", to: "/admin/soporte" };

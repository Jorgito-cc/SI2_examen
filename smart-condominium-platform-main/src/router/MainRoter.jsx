// src/routes/MainRouter.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
// (Opcional) Crea este layout si quieres separar guardia:
import { GuardLayout } from "../layout/GuardLayout";
import { Login } from "../components/Login";
import ProtectedRoutes from "./ProtectRoutes";
import { MainLayout } from "../layout/MainLayout";
import AdminLayout from "../layout/AdminLayout";
import BitacoraPage from "../admin/pages/BitacoraPage";
import PersonalPage from "../admin/pages/PersonalPage";
import UnidadesPage from "../admin/pages/UnidadesPage";
import ResidentesPage from "../admin/pages/ResidentesPage";
import { FormPersonal } from "../admin/pages/FormPersonal";
import { FormUnidades } from "../admin/pages/FormUnidades";
import { FormResidentes } from "../admin/pages/FormResidentes";

export default function MainRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Público */}
        <Route path="/" element={<MainLayout />}>
          {/* Ejemplos de páginas públicas */}

          <Route path="login" element={<Login />} />
        </Route>

        {/* Admin */}
        <Route
          path="/admin"
          element={
            <ProtectedRoutes  allowedRoles={["ADMINISTRADOR"]}>
              <AdminLayout />
            </ProtectedRoutes>
          }
        >
          <Route path="bitacoraPage" element={<BitacoraPage />} />
          <Route path="personalPage" element={<PersonalPage />} />

          <Route path="residentespages" element={<ResidentesPage />} />

          <Route path="unidadpage" element={<UnidadesPage />} />
                    <Route path="registrarpersonal" element={<FormPersonal />} />

          <Route path="registrarunidades" element={<FormUnidades />} />

          <Route path="registrarresidentes" element={<FormResidentes />} />

        </Route>

        {/* Guardia */}
        <Route
          path="/guardia"
          element={
            <ProtectedRoutes allowedRoles={["GUARDIA"]}>
              <GuardLayout />
            </ProtectedRoutes>
          }
        >
          <Route index element={<h1>Panel Guardia</h1>} />
          {/* Ejemplos: control de accesos, lecturas OCR, etc. */}
          <Route path="accesos" element={<h1>Accesos</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

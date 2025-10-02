// NotificacionesPage.jsx
import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";

/* =========================
   CONFIG
   ========================= */
const BASE_URL = "https://backend-condominio-production.up.railway.app/api";
const TOKEN_KEY = "auth_token"; // donde guardas el JWT

/* =========================
   AXIOS INSTANCE con token
   ========================= */
const api = axios.create({
  baseURL: BASE_URL,
  headers: { Accept: "application/json", "Content-Type": "application/json" },
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

/* =========================
   API helpers
   ========================= */
const normalizeList = (data) =>
  Array.isArray(data) ? { results: data, count: data.length, next: null, previous: null }
                      : { results: data.results ?? [], count: data.count ?? data.length ?? 0, next: data.next, previous: data.previous };

async function listNotificaciones({ search = "", leido, ordering = "-creado_en", pageUrl } = {}) {
  // soporta paginación DRF via next/previous URLs
  const params = {};
  if (search) params.search = search;
  if (typeof leido === "boolean") params.leido = leido ? "true" : "false";
  if (ordering) params.ordering = ordering;

  const url = pageUrl ? pageUrl : "/notificaciones/";
  const { data } = await api.get(url, { params });
  return normalizeList(data);
}

async function createNotificacion({ titulo, poligono, descripcion, usuario_id }) {
  const payload = { titulo, poligono, descripcion };
  if (usuario_id) payload.usuario_id = usuario_id; // solo admins
  const { data } = await api.post("/notificaciones/", payload);
  return data;
}

async function updateNotificacion(id, { titulo, poligono, descripcion, leido }) {
  const payload = { titulo, poligono, descripcion, leido };
  const { data } = await api.patch(`/notificaciones/${id}/`, payload);
  return data;
}

async function deleteNotificacion(id) {
  await api.delete(`/notificaciones/${id}/`);
}

async function marcarLeida(id) {
  const { data } = await api.post(`/notificaciones/${id}/marcar_leida/`);
  return data;
}
async function marcarNoLeida(id) {
  const { data } = await api.post(`/notificaciones/${id}/marcar_no_leida/`);
  return data;
}

/* =========================
   UI helpers
   ========================= */
function cls(...xs) {
  return xs.filter(Boolean).join(" ");
}
function fmtDate(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString();
  } catch {
    return iso;
  }
}

/* =========================
   COMPONENTE ÚNICO
   ========================= */
export default function NotificacionesPage() {
  const [items, setItems] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [leido, setLeido] = useState("all"); // all | true | false
  const [ordering, setOrdering] = useState("-creado_en");
  const [nextUrl, setNextUrl] = useState(null);
  const [prevUrl, setPrevUrl] = useState(null);

  // modal state
  const emptyForm = { id: null, titulo: "", poligono: "", descripcion: "" };
  const [form, setForm] = useState(emptyForm);
  const [showModal, setShowModal] = useState(false);
  const isEditing = useMemo(() => form.id !== null, [form]);

  async function load(pageUrl) {
    setLoading(true);
    try {
      const data = await listNotificaciones({
        search: q.trim(),
        leido: leido === "all" ? undefined : leido === "true",
        ordering,
        pageUrl,
      });
      setItems(data.results);
      setCount(data.count);
      setNextUrl(data.next);
      setPrevUrl(data.previous);
    } catch (e) {
      console.error(e);
      alert(e?.response?.data?.detail || "Error cargando notificaciones");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ordering]);

  const onSearch = (e) => {
    e.preventDefault();
    load();
  };

  const openCreate = () => {
    setForm(emptyForm);
    setShowModal(true);
  };
  const openEdit = (n) => {
    setForm({
      id: n.id,
      titulo: n.titulo || "",
      poligono: n.poligono || "",
      descripcion: n.descripcion || "",
    });
    setShowModal(true);
  };

  async function saveForm() {
    try {
      if (isEditing) {
        const updated = await updateNotificacion(form.id, form);
        setItems((xs) => xs.map((x) => (x.id === updated.id ? updated : x)));
      } else {
        const created = await createNotificacion(form);
        setItems((xs) => [created, ...xs]);
        setCount((c) => c + 1);
      }
      setShowModal(false);
    } catch (e) {
      console.error(e);
      alert(e?.response?.data?.detail || "No se pudo guardar");
    }
  }

  async function onDelete(id) {
    if (!window.confirm("¿Eliminar notificación?")) return;
    try {
      await deleteNotificacion(id);
      setItems((xs) => xs.filter((x) => x.id !== id));
      setCount((c) => Math.max(0, c - 1));
    } catch (e) {
      console.error(e);
      alert(e?.response?.data?.detail || "No se pudo eliminar");
    }
  }

  async function toggleLeido(n) {
    try {
      const updated = n.leido ? await marcarNoLeida(n.id) : await marcarLeida(n.id);
      setItems((xs) => xs.map((x) => (x.id === n.id ? updated : x)));
    } catch (e) {
      console.error(e);
      alert("No se pudo cambiar estado de leído");
    }
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <header className="mb-6 flex items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">Notificaciones</h1>
        <button
          onClick={openCreate}
          className="rounded-md bg-blue-600 text-white px-4 py-2 hover:bg-blue-700"
        >
          Nueva
        </button>
      </header>

      {/* Filtros */}
      <form onSubmit={onSearch} className="mb-4 grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar (título, descripción, polígono, usuario)"
          className="border rounded-md px-3 py-2 w-full"
        />

        <select
          value={leido}
          onChange={(e) => setLeido(e.target.value)}
          className="border rounded-md px-3 py-2 w-full"
        >
          <option value="all">Todos</option>
          <option value="false">No leídos</option>
          <option value="true">Leídos</option>
        </select>

        <select
          value={ordering}
          onChange={(e) => setOrdering(e.target.value)}
          className="border rounded-md px-3 py-2 w-full"
        >
          <option value="-creado_en">Recientes primero</option>
          <option value="creado_en">Antiguos primero</option>
          <option value="titulo">Título A→Z</option>
          <option value="-titulo">Título Z→A</option>
          <option value="leido">Leído primero</option>
          <option value="-leido">No leído primero</option>
        </select>

        <div className="flex gap-2">
          <button
            type="submit"
            className="rounded-md bg-gray-800 text-white px-4 py-2 hover:bg-black"
          >
            Buscar
          </button>
          <button
            type="button"
            onClick={() => {
              setQ("");
              setLeido("all");
              setOrdering("-creado_en");
              load();
            }}
            className="rounded-md border px-4 py-2"
          >
            Limpiar
          </button>
        </div>
      </form>

      {/* Tabla */}
      <div className="overflow-x-auto border rounded-lg">
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Título</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Polígono</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Descripción</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Usuario</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Creado</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">Leído</th>
              <th className="px-3 py-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={7} className="p-6 text-center">
                  Cargando…
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-6 text-center">
                  Sin resultados
                </td>
              </tr>
            ) : (
              items.map((n) => (
                <tr key={n.id} className={cls(n.leido ? "bg-white" : "bg-yellow-50")}>
                  <td className="px-3 py-2">{n.titulo}</td>
                  <td className="px-3 py-2">{n.poligono}</td>
                  <td className="px-3 py-2 max-w-[420px]">
                    <div className="line-clamp-2">{n.descripcion}</div>
                  </td>
                  <td className="px-3 py-2">
                    {n.usuario?.username || n.usuario?.email || "—"}
                  </td>
                  <td className="px-3 py-2">{fmtDate(n.creado_en)}</td>
                  <td className="px-3 py-2">
                    <span
                      className={cls(
                        "inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium",
                        n.leido ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                      )}
                    >
                      {n.leido ? "Sí" : "No"}
                    </span>
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex gap-2">
                      <button
                        onClick={() => toggleLeido(n)}
                        className="px-2 py-1 rounded border hover:bg-gray-50"
                        title={n.leido ? "Marcar NO leída" : "Marcar leída"}
                      >
                        {n.leido ? "No leída" : "Leída"}
                      </button>
                      <button
                        onClick={() => openEdit(n)}
                        className="px-2 py-1 rounded border hover:bg-gray-50"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => onDelete(n.id)}
                        className="px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700"
                      >
                        Borrar
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginación */}
      <div className="mt-4 flex items-center justify-between">
        <p className="text-sm text-gray-600">Total: {count}</p>
        <div className="flex gap-2">
          <button
            disabled={!prevUrl}
            onClick={() => load(prevUrl)}
            className={cls(
              "px-3 py-1 rounded border",
              prevUrl ? "hover:bg-gray-50" : "opacity-50 cursor-not-allowed"
            )}
          >
            ← Anterior
          </button>
          <button
            disabled={!nextUrl}
            onClick={() => load(nextUrl)}
            className={cls(
              "px-3 py-1 rounded border",
              nextUrl ? "hover:bg-gray-50" : "opacity-50 cursor-not-allowed"
            )}
          >
            Siguiente →
          </button>
        </div>
      </div>

      {/* Modal Crear/Editar */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg w-full max-w-xl">
            <div className="p-4 border-b flex items-center justify-between">
              <h2 className="text-lg font-semibold">
                {isEditing ? "Editar notificación" : "Nueva notificación"}
              </h2>
              <button onClick={() => setShowModal(false)} className="text-gray-500">
                ✕
              </button>
            </div>
            <div className="p-4 space-y-3">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Título"
                value={form.titulo}
                onChange={(e) => setForm((f) => ({ ...f, titulo: e.target.value }))}
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Polígono"
                value={form.poligono}
                onChange={(e) => setForm((f) => ({ ...f, poligono: e.target.value }))}
              />
              <textarea
                className="w-full border rounded px-3 py-2 min-h-[120px]"
                placeholder="Descripción"
                value={form.descripcion}
                onChange={(e) => setForm((f) => ({ ...f, descripcion: e.target.value }))}
              />
            </div>
            <div className="p-4 border-t flex justify-end gap-2">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 rounded border">
                Cancelar
              </button>
              <button
                onClick={saveForm}
                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
              >
                {isEditing ? "Guardar" : "Crear"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

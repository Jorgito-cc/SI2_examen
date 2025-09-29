import { useEffect, useState, useCallback } from "react";
import { toast } from "react-toastify";
import { getResidentes } from "../../api/residentes";

export default function ResidentesPage() {
  const [residentes, setResidentes] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getResidentes();
      setResidentes(data);
      toast.success(`Residentes cargados: ${data.length}`);
    } catch (err) {
      console.error(err);
      toast.error("No se pudieron cargar los residentes");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <section className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">👨‍👩‍👧 Residentes</h1>
        <button
          onClick={load}
          className="px-3 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
        >
          Refrescar
        </button>
      </div>

      {loading ? (
        <div className="p-6 text-sm text-gray-500">Cargando…</div>
      ) : residentes.length === 0 ? (
        <div className="p-6 text-sm text-gray-500 border rounded-xl bg-gray-50">
          No hay residentes registrados.
        </div>
      ) : (
        <div className="overflow-x-auto bg-white rounded-xl border">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-3 py-2 text-left">ID</th>
                <th className="border px-3 py-2 text-left">Usuario</th>
                <th className="border px-3 py-2 text-left">Rol</th>
                <th className="border px-3 py-2 text-left">Unidad</th>
              </tr>
            </thead>
            <tbody>
              {residentes.map((r) => (
                <tr key={r.id} className="hover:bg-gray-50">
                  <td className="border px-3 py-2">{r.id}</td>
                  <td className="border px-3 py-2">
                    {r.usuario?.username || r.username || "—"}
                  </td>
                  <td className="border px-3 py-2">
                    {Array.isArray(r.usuario?.roles)
                      ? r.usuario.roles.map(ro => ro.nombre).join(", ")
                      : (r.rol_nombre || "—")}
                  </td>
                  <td className="border px-3 py-2">
                    {r.unidad?.codigo || r.unidad_id || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

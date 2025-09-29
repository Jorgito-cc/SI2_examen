import { useEffect, useState, useCallback } from "react";
import { toast } from "react-toastify";
import { getUnidades } from "../../api/unidades";

export default function UnidadesPage() {
  const [unidades, setUnidades] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getUnidades();
      setUnidades(data);
      toast.success(`Unidades cargadas: ${data.length}`);
    } catch (err) {
      console.error(err);
      toast.error("No se pudieron cargar las unidades");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  return (
    <section className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">🏢 Unidades Habitacionales</h1>
        <button
          onClick={load}
          className="px-3 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
        >
          Refrescar
        </button>
      </div>

      {loading ? (
        <div className="p-6 text-sm text-gray-500">Cargando…</div>
      ) : unidades.length === 0 ? (
        <div className="p-6 text-sm text-gray-500 border rounded-xl bg-gray-50">
          No hay unidades registradas.
        </div>
      ) : (
        <div className="overflow-x-auto bg-white rounded-xl border">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-3 py-2 text-left">ID</th>
                <th className="border px-3 py-2 text-left">Código</th>
                <th className="border px-3 py-2 text-left">Descripción</th>
                <th className="border px-3 py-2 text-left">Piso</th>
                <th className="border px-3 py-2 text-left">Torre</th>
                <th className="border px-3 py-2 text-left">Estado</th>
              </tr>
            </thead>
            <tbody>
              {unidades.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50">
                  <td className="border px-3 py-2">{u.id}</td>
                  <td className="border px-3 py-2">{u.codigo ?? `B${u.bloque ?? "?"}-${u.numero ?? "?"}`}</td>
                  <td className="border px-3 py-2">{u.descripcion ?? "—"}</td>
                  <td className="border px-3 py-2">{u.piso ?? "—"}</td>
                  <td className="border px-3 py-2">{u.torre ?? u.bloque ?? "—"}</td>
                  <td className="border px-3 py-2">{u.estado ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

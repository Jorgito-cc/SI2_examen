import { useEffect, useMemo, useState } from "react";
import { getBitacora } from "../../api";
// Si quieres exportar:
// import jsPDF from "jspdf";
// import autoTable from "jspdf-autotable";
// import * as XLSX from "xlsx";
// import { saveAs } from "file-saver";

function fmtDate(iso) {
  try { const d = new Date(iso); return d.toISOString().slice(0,10); } catch { return ""; }
}
function fmtTime(iso) {
  try { const d = new Date(iso); return d.toTimeString().slice(0,8); } catch { return ""; }
}

export default function BitacoraPage() {
  const [q, setQ] = useState("");         // busca en acción/detalle/path (lo hace el backend)
  const [fecha, setFecha] = useState(""); // atajo: manda desde = hasta = fecha
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [rows, setRows] = useState([]);

  const filtros = useMemo(() => {
    const f = { q };
    if (fecha) { f.desde = fecha; f.hasta = fecha; }
    return f;
  }, [q, fecha]);

  const load = async () => {
    setLoading(true); setErr(null);
    try {
      const data = await getBitacora(filtros);
      setRows(data.results || data); // por si no usas paginación DRF
    } catch (e) {
      setErr(e?.response?.data?.detail || e?.message || "Error al cargar bitácora");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, []);

  // Si deseas exportar, descomenta y usa:
  // const exportarPDF = () => {
  //   const doc = new jsPDF();
  //   doc.text("Bitácora", 14, 14);
  //   autoTable(doc, {
  //     head: [["ID","Usuario","Acción","IP","Fecha","Hora","Ruta"]],
  //     body: rows.map(r => [r.id, r.usuario ?? "", r.accion ?? "", r.ip ?? "", fmtDate(r.creado_en), fmtTime(r.creado_en), r.path ?? ""])
  //   });
  //   doc.save("bitacora.pdf");
  // };
  // const exportarExcel = () => {
  //   const data = rows.map(r => ({
  //     id: r.id, usuario: r.usuario, accion: r.accion, detalle: r.detalle,
  //     ip: r.ip, path: r.path, user_agent: r.user_agent,
  //     fecha: fmtDate(r.creado_en), hora: fmtTime(r.creado_en)
  //   }));
  //   const ws = XLSX.utils.json_to_sheet(data);
  //   const wb = XLSX.utils.book_new();
  //   XLSX.utils.book_append_sheet(wb, ws, "Bitacora");
  //   const buf = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  //   saveAs(new Blob([buf], { type: "application/octet-stream" }), "bitacora.xlsx");
  // };

  return (
    <section className="space-y-6">
      <header className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-slate-900 dark:text-slate-100">Bitácora</h1>
          <p className="text-slate-600 dark:text-slate-400">Registros de acciones del sistema</p>
        </div>
        {/* Botones export (si activas) */}
        {/* <div className="flex gap-2">
          <button onClick={exportarExcel} className="px-3 py-2 rounded-xl border">Excel</button>
          <button onClick={exportarPDF} className="px-3 py-2 rounded-xl border">PDF</button>
        </div> */}
      </header>

      {/* Filtros */}
      <form
        onSubmit={(e)=>{ e.preventDefault(); load(); }}
        className="grid grid-cols-1 md:grid-cols-3 gap-3"
      >
        <input
          value={q}
          onChange={e=>setQ(e.target.value)}
          placeholder="Buscar (acción, detalle, ruta)"
          className="px-3 py-2 rounded-xl border bg-white/70 dark:bg-slate-800/70 border-slate-300 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <input
          type="date"
          value={fecha}
          onChange={e=>setFecha(e.target.value)}
          className="px-3 py-2 rounded-xl border bg-white/70 dark:bg-slate-800/70 border-slate-300 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <div className="flex gap-2">
          <button className="flex-1 px-3 py-2 rounded-xl bg-indigo-600 text-white font-medium hover:bg-indigo-700">
            Buscar
          </button>
          <button
            type="button"
            onClick={()=>{ setQ(""); setFecha(""); load(); }}
            className="px-3 py-2 rounded-xl border font-medium bg-white/70 dark:bg-slate-800/70"
          >
            Limpiar
          </button>
        </div>
      </form>

      {/* Tabla */}
      <div className="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60">
        <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
          <thead className="bg-slate-50/60 dark:bg-slate-900/40">
            <tr>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">ID</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Usuario</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Acción</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">IP</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Fecha</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Hora</th>
              <th className="px-3 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Ruta</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {loading && (
              <>
                <tr className="animate-pulse"><td className="p-3" colSpan={7}><div className="h-4 w-full rounded bg-slate-200" /></td></tr>
                <tr className="animate-pulse"><td className="p-3" colSpan={7}><div className="h-4 w-full rounded bg-slate-200" /></td></tr>
              </>
            )}

            {!loading && err && (
              <tr><td colSpan={7} className="p-6 text-center text-red-600">{err}</td></tr>
            )}

            {!loading && !err && rows.length === 0 && (
              <tr><td colSpan={7} className="p-6 text-center text-slate-500">Sin registros.</td></tr>
            )}

            {!loading && !err && rows.map((r) => (
              <tr key={r.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                <td className="p-3 align-top">{r.id}</td>
                <td className="p-3 align-top">{r.usuario ?? <i className="text-slate-400">system</i>}</td>
                <td className="p-3 align-top">
                  <div className="text-sm font-medium text-slate-900 dark:text-slate-100">{r.accion}</div>
                  {r.detalle && <div className="text-xs text-slate-600 dark:text-slate-400">{r.detalle}</div>}
                  {r.user_agent && <div className="mt-1"><span className="text-[11px] text-slate-500">{r.user_agent}</span></div>}
                </td>
                <td className="p-3 align-top">{r.ip || "—"}</td>
                <td className="p-3 align-top">{fmtDate(r.creado_en)}</td>
                <td className="p-3 align-top">{fmtTime(r.creado_en)}</td>
                <td className="p-3 align-top"><code className="text-xs bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">{r.path || "—"}</code></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

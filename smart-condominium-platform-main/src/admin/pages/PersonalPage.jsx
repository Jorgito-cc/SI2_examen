import { useEffect, useState, useCallback } from "react";
import { toast } from "react-toastify";
import { getPersonal } from "../../api/personal";

export default function PersonalPage() {
  const [personal, setPersonal] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getPersonal();
      setPersonal(data);
      toast.success(`Personal cargado: ${data.length}`);
    } catch (err) {
      console.error(err);
      toast.error("No se pudo cargar el personal");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <section className="p-6 space-y-4">
      <div className="flex items-center justify-between">
<h1 className="text-2xl font-bold">👷 Personal</h1>
        <button
          onClick={load}
          className="px-3 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
        >
   Refrescar 
        </button>
      
      </div>
      
      {loading ? (
        <div className="p-6 text-sm text-gray-500">Cargando…</div>
      ) : personal.length === 0 ? (
        <div className="p-6 text-sm text-gray-500 border rounded-xl bg-gray-50">
        No hay personal registrado. 
        </div>
      ) : (
        <div className="overflow-x-auto bg-white rounded-xl border">
      
          <table className="min-w-full text-sm">
       
            <thead className="bg-gray-100">
       
              <tr>
                {/* COLUMNAS AÑADIDAS */}
                <th className="border px-3 py-2 text-left">ID</th>
                 <th className="border px-3 py-2 text-left">Foto</th>
             
                <th className="border px-3 py-2 text-left">Nombre Completo</th>
            
                <th className="border px-3 py-2 text-left">Email</th>
                 <th className="border px-3 py-2 text-left">Usuario</th>
               
          <th className="border px-3 py-2 text-left">Rol</th>

                <th className="border px-3 py-2 text-left">Entrada</th>
            <th className="border px-3 py-2 text-left">Salida</th>
             
              </tr>
             
            </thead>
        
            <tbody>
         
              {personal.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
               <td className="border px-3 py-2">{p.id}</td>
                  {/* CELDA DE FOTO (p.usuario?.url_img) */}
                  <td className="border px-3 py-2">
                    {p.usuario?.url_img ? (
                      <img
                        src={p.usuario.url_img}
                        alt="Foto"
                        className="w-8 h-8 rounded-full object-cover"
                      />
                    ) : (
                      <span className="text-gray-400">N/A</span>
                    )}
                  </td>
                  {/* CELDA NOMBRE COMPLETO */}
                  <td className="border px-3 py-2">
                    {p.usuario?.first_name} {p.usuario?.last_name}
                  </td>
                  {/* CELDA EMAIL */}
                  <td className="border px-3 py-2">
                    {p.usuario?.email || "—"}
                  </td>
                  <td className="border px-3 py-2">
                    {p.usuario?.username || p.username || "—"}
                  </td>
                  <td className="border px-3 py-2">{p.ocupacion ?? "—"}</td>
                  {/* CELDA ROL */}
                  <td className="border px-3 py-2">{p.rol_nombre ?? "—"}</td>
                  <td className="border px-3 py-2">
                    {p.horario_entrada ?? "—"}
                  </td>
                  <td className="border px-3 py-2">
                    {p.horario_salida ?? "—"}
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
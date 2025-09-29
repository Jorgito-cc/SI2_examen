import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import { createUnidad, updateUnidad, deleteUnidad } from "../../api/unidades";
import { useState } from "react";

export const FormUnidades = ({ id = null, defaultValues = {}, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const isEdit = Boolean(id);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    mode: "onTouched",
    defaultValues: {
      bloque: "",
      numero: "",
      estado: "ACTIVA",
      superficie: "",
      ...defaultValues,
    },
  });

  const onSubmit = async (values) => {
    try {
      setLoading(true);
      // superficie a null si viene vacío
      const payload = {
        ...values,
        superficie: values.superficie === "" ? null : values.superficie,
      };

      const res = isEdit
        ? await updateUnidad(id, payload)
        : await createUnidad(payload);

      toast.success(isEdit ? "Unidad actualizada" : "Unidad creada");
      onSuccess?.(res);
    } catch (e) {
      console.error(e);
      toast.error("Error al guardar unidad");
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!isEdit) return;
    if (!confirm("¿Eliminar esta unidad?")) return;
    try {
      setLoading(true);
      await deleteUnidad(id);
      toast.success("Unidad eliminada");
      onSuccess?.({ deleted: true });
    } catch (e) {
      console.error(e);
      toast.error("Error al eliminar unidad");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-4">
      <h2 className="text-xl font-semibold">
        {isEdit ? "Editar unidad" : "Nueva unidad"}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Bloque</label>
          <input
            className="w-full px-3 py-2 rounded-lg border"
            {...register("bloque", { required: "Bloque requerido" })}
            placeholder="A"
          />
          {errors.bloque && (
            <p className="text-sm text-red-600 mt-1">{errors.bloque.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Número</label>
          <input
            className="w-full px-3 py-2 rounded-lg border"
            {...register("numero", { required: "Número requerido" })}
            placeholder="101"
          />
          {errors.numero && (
            <p className="text-sm text-red-600 mt-1">{errors.numero.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Estado</label>
          <select
            className="w-full px-3 py-2 rounded-lg border"
            {...register("estado", { required: "Estado requerido" })}
          >
            <option value="ACTIVA">ACTIVA</option>
            <option value="INACTIVA">INACTIVA</option>
          </select>
          {errors.estado && (
            <p className="text-sm text-red-600 mt-1">{errors.estado.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Superficie (m²)</label>
          <input
            type="number"
            step="0.01"
            className="w-full px-3 py-2 rounded-lg border"
            {...register("superficie")}
            placeholder="80.50"
          />
        </div>
      </div>

      <div className="flex gap-2">
        <button
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-60"
        >
          {isEdit ? "Actualizar" : "Crear"}
        </button>
        {isEdit && (
          <button
            type="button"
            onClick={onDelete}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-60"
          >
            Eliminar
          </button>
        )}
      </div>
    </form>
  );
};

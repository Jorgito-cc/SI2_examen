import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import { createResidente, updateResidente, deleteResidente } from "../../api/residentes";
import { useState } from "react";

/**
 * Tips:
 * - Crear: manda username/password + rol_nombre + unidad_id (o usuario_id si ya existe)
 * - Editar: normalmente actualizarás rol_nombre y/o unidad_id
 */
export const FormResidentes = ({ id = null, defaultValues = {}, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const isEdit = Boolean(id);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm({
    mode: "onTouched",
    defaultValues: {
      // Camino B (crear nuevo usuario)
      username: "",
      password: "",
      email: "",
      first_name: "",
      last_name: "",
      ci: "",
      telefono: "",
      // Rol y unidad
      rol_nombre: "PROPIETARIO",
      unidad_id: "",
      // Si usas usuario existente:
      // usuario_id: null,
      ...defaultValues,
    },
  });

  const usuarioId = watch("usuario_id");
  const username = watch("username");

  const onSubmit = async (values) => {
    try {
      setLoading(true);

      // Normaliza payload:
      const payload = { ...values };

      // Si se elige usuario existente, borra credenciales para no confundir al backend
      if (usuarioId) {
        delete payload.username;
        delete payload.password;
      }

      // Si NO es edición => crear
      if (!isEdit) {
        // Validación mínima de front: necesitas usuario_id O (username+password)
        const creandoUsuario = payload.username && payload.password;
        const usandoExistente = !!payload.usuario_id;
        if (!creandoUsuario && !usandoExistente) {
          toast.error("Debes enviar usuario existente o username+password");
          setLoading(false);
          return;
        }
        const res = await createResidente(payload);
        toast.success("Residente creado");
        onSuccess?.(res);
        return;
      }

      // Edición: manda solo campos que tu backend acepte (rol / unidad / algunos datos del usuario)
      // Puedes ajustar según tu caso:
      const minimal = {
        rol_nombre: payload.rol_nombre,
        unidad_id: payload.unidad_id,
      };
      const res = await updateResidente(id, minimal);
      toast.success("Residente actualizado");
      onSuccess?.(res);
    } catch (e) {
      console.error(e);
      toast.error("Error al guardar residente");
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!isEdit) return;
    if (!confirm("¿Eliminar este residente?")) return;
    try {
      setLoading(true);
      await deleteResidente(id);
      toast.success("Residente eliminado");
      onSuccess?.({ deleted: true });
    } catch (e) {
      console.error(e);
      toast.error("Error al eliminar residente");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-4">
      <h2 className="text-xl font-semibold">
        {isEdit ? "Editar residente" : "Nuevo residente"}
      </h2>

      {/* Selector: usar usuario existente (usuario_id) o crear nuevo (username+password) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">
            Usuario existente (ID) — opcional
          </label>
          <input
            type="number"
            className="w-full px-3 py-2 rounded-lg border"
            {...register("usuario_id")}
            placeholder="Ej: 12"
          />
          <p className="text-xs text-gray-500 mt-1">
            Si completas este campo, no es necesario llenar username/password.
          </p>
        </div>

        <div className="md:col-span-2 border-t pt-3" />

        <div>
          <label className="block text-sm font-medium mb-1">Username (crear)</label>
          <input
            className="w-full px-3 py-2 rounded-lg border"
            {...register("username", {
              validate: v => (!!watch("usuario_id") || !!v) || "Ingresa username o usuario_id",
            })}
            disabled={!!usuarioId}
            placeholder="jdoe"
          />
          {errors.username && (
            <p className="text-sm text-red-600 mt-1">{errors.username.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Password (crear)</label>
          <input
            type="password"
            className="w-full px-3 py-2 rounded-lg border"
            {...register("password", {
              validate: v => (!!watch("usuario_id") || !!watch("username") ? !!v : true) || "Password requerido",
              minLength: { value: 6, message: "Mínimo 6 caracteres" },
            })}
            disabled={!!usuarioId}
            placeholder="••••••••"
          />
          {errors.password && (
            <p className="text-sm text-red-600 mt-1">{errors.password.message}</p>
          )}
        </div>

        {/* Datos extra del usuario (opcionales si creas nuevo) */}
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input className="w-full px-3 py-2 rounded-lg border" {...register("email")} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Nombres</label>
          <input className="w-full px-3 py-2 rounded-lg border" {...register("first_name")} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Apellidos</label>
          <input className="w-full px-3 py-2 rounded-lg border" {...register("last_name")} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">CI</label>
          <input className="w-full px-3 py-2 rounded-lg border" {...register("ci")} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Teléfono</label>
          <input className="w-full px-3 py-2 rounded-lg border" {...register("telefono")} />
        </div>

        {/* Rol + Unidad */}
        <div>
          <label className="block text-sm font-medium mb-1">Rol</label>
          <select
            className="w-full px-3 py-2 rounded-lg border"
            {...register("rol_nombre", { required: "Rol requerido" })}
          >
            <option value="PROPIETARIO">PROPIETARIO</option>
            <option value="INQUILINO">INQUILINO</option>
          </select>
          {errors.rol_nombre && (
            <p className="text-sm text-red-600 mt-1">{errors.rol_nombre.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Unidad (ID)</label>
          <input
            type="number"
            className="w-full px-3 py-2 rounded-lg border"
            {...register("unidad_id", { required: "Unidad requerida" })}
            placeholder="Ej: 5"
          />
          {errors.unidad_id && (
            <p className="text-sm text-red-600 mt-1">{errors.unidad_id.message}</p>
          )}
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

import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import { createPersonal, updatePersonal, deletePersonal } from "../../api/personal";
import { useState } from "react";

// Función de Cloudinary (idealmente estaría en un utils/cloud.js)
const subirImagenACloudinary = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "reactproyecto"); 

   const res = await fetch("https://api.cloudinary.com/v1_1/dyqbimuzw/image/upload", {
        method: "POST",
        body: formData,
    });

    if (!res.ok) throw new Error("Error al subir imagen a Cloudinary");

    const data = await res.json();
    return data.secure_url; 
};

export const FormPersonal = ({ id = null, defaultValues = {}, onSuccess }) => {
    const [loading, setLoading] = useState(false);
    // Estado para la previsualización de la nueva imagen
    const [imagenPreview, setImagenPreview] = useState(null);
    const isEdit = Boolean(id);

    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
    } = useForm({
        mode: "onTouched",
        defaultValues: {
            username: "",
            password: "",
            email: "",
            first_name: "",
            last_name: "",
            ocupacion: "",
            horario_entrada: "",
            horario_salida: "",
            rol_nombre: "PERSONAL",
            // Establece la imagen de usuario existente como preview inicial
            // El campo 'url_img' viene en defaultValues si es edición
            ...defaultValues, 
        },
    });

    const isChangingPassword = watch("password");
    // Observar el campo de archivo para la previsualización
    const imagenFile = watch("imagen");
    
    // Lógica de previsualización para el campo de archivo
    useState(() => {
        if (imagenFile && imagenFile.length > 0) {
            setImagenPreview(URL.createObjectURL(imagenFile[0]));
        } else if (isEdit && defaultValues.url_img) {
            // Mostrar la imagen existente si no hay archivo nuevo
            setImagenPreview(defaultValues.url_img);
        } else {
            setImagenPreview(null);
        }
    }, [imagenFile, isEdit, defaultValues.url_img]);

    const onSubmit = async (values) => {
        try {
            setLoading(true);

            let urlImg = values.url_img || ""; // Usa la URL existente por defecto
            
            // 1. Subir nueva imagen si se seleccionó un archivo
            const file = values.imagen && values.imagen[0];
            if (file) {
                toast.info("Subiendo imagen...", { autoClose: 1500 });
                urlImg = await subirImagenACloudinary(file);
            }
            
            // 2. Preparar el payload
            const payload = { 
                ...values,
                url_img: urlImg, // Añade la URL (nueva o existente) al payload
            };
            
            // 3. Limpiar datos que no van al backend
            delete payload.imagen; // Eliminar el objeto FileList
            if (isEdit && !payload.password) delete payload.password;

            // 4. Llamada a la API
            const res = isEdit
                ? await updatePersonal(id, payload)
                : await createPersonal(payload);

            toast.success(isEdit ? "Personal actualizado" : "Personal creado");
            onSuccess?.(res);
        } catch (e) {
            console.error(e);
            toast.error("Error al guardar personal. Revisa la consola.");
        } finally {
            setLoading(false);
        }
    };
    
    // ... (onDelete logic remains the same) ...

    const onDelete = async () => {
        if (!isEdit) return;
        if (!confirm("¿Eliminar este registro de personal?")) return;
        try {
            setLoading(true);
            await deletePersonal(id);
            toast.success("Personal eliminado");
            onSuccess?.({ deleted: true });
        } catch (e) {
            console.error(e);
            toast.error("Error al eliminar personal");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-4">
            <h2 className="text-xl font-semibold">
                {isEdit ? "Editar personal" : "Nuevo personal"}
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {/* Campos existentes (username, password, email, first_name, last_name, ocupacion, horarios...) */}
                {/* ... (resto de tus inputs) ... */}
                
                {/* Campo URL_IMG - Input Oculto para la edición */}
                {isEdit && <input type="hidden" {...register("url_img")} />}

                {/* Nuevo campo para subir la imagen de perfil */}
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium mb-1">Imagen de Perfil</label>
                    <input
                        type="file"
                        accept="image/*"
                        className="w-full px-3 py-2 rounded-lg border file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                        {...register("imagen", {
                            required: !isEdit && "Imagen requerida para nuevo personal", // Requerida solo en creación
                        })}
                    />
                    {errors.imagen && (
                        <p className="text-sm text-red-600 mt-1">{errors.imagen.message}</p>
                    )}
                    
                    {/* Previsualización de la imagen */}
                    {(imagenPreview || isEdit && defaultValues.url_img) && (
                        <div className="mt-3">
                            <img 
                                src={imagenPreview || defaultValues.url_img} 
                                alt="Previsualización" 
                                className="w-24 h-24 object-cover rounded-full border-2 border-indigo-500" 
                            />
                        </div>
                    )}
                </div>
                
                {/* Campos existentes */}
                <div>
                  <label className="block text-sm font-medium mb-1">Usuario</label>
                  <input
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("username", { required: "Usuario requerido" })}
                    placeholder="guardia1"
                    disabled={isEdit}
                  />
                  {errors.username && (
                    <p className="text-sm text-red-600 mt-1">{errors.username.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    {isEdit ? "Cambiar contraseña (opcional)" : "Contraseña"}
                  </label>
                  <input
                    type="password"
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("password", {
                      validate: v => (!isEdit || !v || v.length >= 6) || "Mínimo 6 caracteres",
                      required: !isEdit ? "Contraseña requerida" : false,
                    })}
                    placeholder="••••••••"
                  />
                  {errors.password && (
                    <p className="text-sm text-red-600 mt-1">{errors.password.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Email</label>
                  <input
                    type="email"
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("email", { required: "Email requerido" })}
                    placeholder="correo@mail.com"
                  />
                  {errors.email && (
                    <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Nombres</label>
                  <input
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("first_name", { required: "Nombres requeridos" })}
                    placeholder="Juan"
                  />
                  {errors.first_name && (
                    <p className="text-sm text-red-600 mt-1">{errors.first_name.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Apellidos</label>
                  <input
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("last_name", { required: "Apellidos requeridos" })}
                    placeholder="Pérez"
                  />
                  {errors.last_name && (
                    <p className="text-sm text-red-600 mt-1">{errors.last_name.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Ocupación</label>
                  <input
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("ocupacion", { required: "Ocupación requerida" })}
                    placeholder="GUARDIA"
                  />
                  {errors.ocupacion && (
                    <p className="text-sm text-red-600 mt-1">{errors.ocupacion.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Entrada</label>
                  <input
                    type="time"
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("horario_entrada", { required: "Hora requerida" })}
                  />
                  {errors.horario_entrada && (
                    <p className="text-sm text-red-600 mt-1">{errors.horario_entrada.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Salida</label>
                  <input
                    type="time"
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("horario_salida", { required: "Hora requerida" })}
                  />
                  {errors.horario_salida && (
                    <p className="text-sm text-red-600 mt-1">{errors.horario_salida.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Rol</label>
                  <select
                    className="w-full px-3 py-2 rounded-lg border"
                    {...register("rol_nombre")}
                  >
                    <option value="PERSONAL">PERSONAL</option>
                    <option value="GUARDIA">GUARDIA</option>
                  </select>
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
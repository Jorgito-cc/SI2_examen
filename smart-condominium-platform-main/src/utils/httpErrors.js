export function getHttpErrorMessage(error) {
  if (error?.response?.data) {
    const d = error.response.data;
    if (typeof d === "string") return d;
    if (d.detail) return d.detail;               // DRF/JWT clásico
    if (d.message) return d.message;
    // Si vienen errores campo a campo:
    const first = Object.values(d)[0];
    if (Array.isArray(first)) return first[0];
    return JSON.stringify(d);
  }
  if (error?.message) return error.message;
  return "Error inesperado. Intenta de nuevo.";
}

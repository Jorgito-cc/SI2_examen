import instance from "./axios";

export async function getBitacora({ q="", desde="", hasta="" } = {}) {
  const params = { q, desde, hasta };
  Object.keys(params).forEach(k => (params[k] ? null : delete params[k]));

  try {
    const { data } = await instance.get("/bitacora/", { params });
    // Paginado DRF o lista simple
    return Array.isArray(data) ? { results: data, count: data.length } : data;
  } catch (e) {
    if (e?.response?.status === 403) {
      const { data } = await instance.get("/bitacora/mias/", { params });
      return Array.isArray(data) ? { results: data, count: data.length } : data;
    }
    throw e;
  }
}
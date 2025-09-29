import instance from "./axios";

export async function getUnidades() {
  const { data } = await instance.get("/unidades/");
  return Array.isArray(data) ? data : data.results || [];
}

export async function createUnidad(payload) {
  const { data } = await instance.post("/unidades/", payload);
  return data;
}

export async function updateUnidad(id, payload) {
  const { data } = await instance.put(`/unidades/${id}/`, payload);
  return data;
}

export async function deleteUnidad(id) {
  await instance.delete(`/unidades/${id}/`);
}

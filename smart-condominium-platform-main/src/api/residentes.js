import instance from "./axios";

export async function getResidentes() {
  const { data } = await instance.get("/residentes/");
  return Array.isArray(data) ? data : data.results || [];
}

export async function createResidente(payload) {
  const { data } = await instance.post("/residentes/", payload);
  return data;
}

export async function updateResidente(id, payload) {
  const { data } = await instance.put(`/residentes/${id}/`, payload);
  return data;
}

export async function deleteResidente(id) {
  await instance.delete(`/residentes/${id}/`);
}

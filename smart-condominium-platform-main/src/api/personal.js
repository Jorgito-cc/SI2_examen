import instance from "./axios";

export async function getPersonal() {
  const { data } = await instance.get("/personal/");
  return Array.isArray(data) ? data : data.results || [];
}

export async function createPersonal(payload) {
  const { data } = await instance.post("/personal/", payload);
  return data;
}

export async function updatePersonal(id, payload) {
  const { data } = await instance.put(`/personal/${id}/`, payload);
  return data;
}

export async function deletePersonal(id) {
  await instance.delete(`/personal/${id}/`);
}

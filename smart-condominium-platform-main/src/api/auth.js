// src/api/auth.js (o donde exportas loginRequest)
import instance from "./axios";

export const loginRequest = async ({ username, password }) => {
  const { data } = await instance.post("/login/", { username, password }, {
    headers: { "Content-Type": "application/json" },
  });
  return data; // { access, refresh?, usuario? }
};
export async function meRequest(accessToken) {
  const { data } = await instance.get("/usuarios/me/", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return data;
}
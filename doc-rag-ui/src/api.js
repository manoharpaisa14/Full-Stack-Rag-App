import axios from 'axios';

const API = axios.create({
  baseURL: "http://localhost:8000", // or wherever your backend lives
});

API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`; // ✅ automatically set token
  }
  return req;
});

export default API;

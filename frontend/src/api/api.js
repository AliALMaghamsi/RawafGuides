import axios from 'axios';

const api  = axios.create({
   baseURL: "http://localhost:8000",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // get token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // add Authorization header
    }
    return config;
  },
  (error) => Promise.reject(error) // handle request error
);

export default api
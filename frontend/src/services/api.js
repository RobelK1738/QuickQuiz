import axios from "axios";
import { getIdToken, onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase";

const waitForUser = () => {
  return new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      unsubscribe();
      resolve(user);
    });
  });
};

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api",
   withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);


export const getPublicQuizzes = () => api.get("/quizzes");
export const getMyQuizzes = () => api.get("/quizzes/my");
export const getQuizById = (id) => api.get(`/quizzes/${id}`);
export const getMyResults = () => api.get("/quizzes/my-results");
export const getAttempt = (attemptId) => api.get(`/quizzes/attempts/${attemptId}`); // <-- NEW
export const createQuiz = (data) => api.post("/quizzes", data);
export const deleteQuiz = (id) => api.delete(`/quizzes/${id}`);
export const updateQuiz = (id, data) => api.put(`/quizzes/${id}`, data);
export const submitQuiz = (id, answers) => api.post(`/quizzes/${id}/submit`, { answers });
export const getMyLatestAttempt = (id) => api.get(`/quizzes/${id}/my-latest-attempt`);


export default api;

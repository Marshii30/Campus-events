import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api/v1",
  timeout: 7000
});

// Events
export const fetchEvents = (params = {}) => API.get("/events", { params });
export const getEvent = (id) => API.get(`/events/${id}`);
export const createEvent = (payload, token) =>
  API.post("/events", payload, { headers: { "X-Admin-Token": token } });

// Registration / attendance / feedback
export const registerEvent = (id, data) => API.post(`/events/${id}/register`, data);
export const markAttendance = (id, data) => API.post(`/events/${id}/attendance`, data);
export const sendFeedback = (id, data) => API.post(`/events/${id}/feedback`, data);

// Reports
export const eventPopularity = (collegeId) =>
  API.get(`/reports/event_popularity`, { params: { college_id: collegeId }});
export const studentParticipation = (collegeId) =>
  API.get(`/reports/student_participation`, { params: { college_id: collegeId }});
export const mostActive = (collegeId, limit = 3) =>
  API.get(`/reports/most_active_students`, { params: { college_id: collegeId, limit }});

// Student registrations listing (by student id)
export const getStudentRegistrations = (studentId) =>
  API.get(`/students/${studentId}/registrations`);

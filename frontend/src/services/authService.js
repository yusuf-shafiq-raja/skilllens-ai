import api from "./api";

// -----------------------------------------------------
// Login
// -----------------------------------------------------

export const loginUser = async (email, password) => {
  const response = await api.post("/auth/login", {
    email,
    password,
  });

  return response.data;
};

// -----------------------------------------------------
// Register
// -----------------------------------------------------

export const registerUser = async (userData) => {
  const response = await api.post("/auth/register", userData);

  return response.data;
};

// -----------------------------------------------------
// Logout
// -----------------------------------------------------

export const logoutUser = () => {
  localStorage.removeItem("access_token");
};

// -----------------------------------------------------
// Save Token
// -----------------------------------------------------

export const saveToken = (token) => {
  localStorage.setItem("access_token", token);
};

// -----------------------------------------------------
// Get Token
// -----------------------------------------------------

export const getToken = () => {
  return localStorage.getItem("access_token");
};

// -----------------------------------------------------
// Check Login
// -----------------------------------------------------

export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};
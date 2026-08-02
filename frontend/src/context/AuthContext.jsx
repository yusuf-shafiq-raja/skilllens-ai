import { createContext, useContext, useEffect, useState } from "react";

import {
  loginUser,
  logoutUser,
  saveToken,
  getToken,
} from "../services/authService";

const AuthContext = createContext();

export function AuthProvider({ children }) {

  const [user, setUser] = useState(null);

  const [loading, setLoading] = useState(true);

  // -----------------------------------------------------
  // Load Existing Login
  // -----------------------------------------------------

  useEffect(() => {

    const token = getToken();

    if (token) {
      setUser({
        token: token
      });
    }

    setLoading(false);

  }, []);

  // -----------------------------------------------------
  // Login
  // -----------------------------------------------------

  const login = async (email, password) => {

    const response = await loginUser(
      email,
      password
    );

    saveToken(
      response.access_token
    );

    setUser({
      token: response.access_token
    });

    return response;
  };

  // -----------------------------------------------------
  // Logout
  // -----------------------------------------------------

  const logout = () => {

    logoutUser();

    setUser(null);

  };

  // -----------------------------------------------------
  // Context
  // -----------------------------------------------------

  return (

    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        loading,
        isAuthenticated: !!user
      }}
    >

      {children}

    </AuthContext.Provider>

  );

}

// -----------------------------------------------------
// Hook
// -----------------------------------------------------

export function useAuth() {
  return useContext(AuthContext);
}
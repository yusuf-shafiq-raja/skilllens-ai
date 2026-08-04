import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";

import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";

import AssessmentList from "./pages/Assessments/AssessmentList";
import AssessmentAttempt from "./pages/Assessments/AssessmentAttempt";
import AssessmentResult from "./pages/Assessments/AssessmentResult";

import Competency from "./pages/Competency/Competency";
import Roadmap from "./pages/Roadmap/Roadmap";
import Resume from "./pages/Resume/Resume";

import PlacementReadiness from "./pages/PlacementReadiness/PlacementReadiness";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>

        <Routes>

          {/* Public */}

          <Route
            path="/"
            element={<Login />}
          />

          {/* Dashboard */}

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Assessments */}

          <Route
            path="/assessments"
            element={
              <ProtectedRoute>
                <AssessmentList />
              </ProtectedRoute>
            }
          />

          <Route
            path="/assessment/:attemptId"
            element={
              <ProtectedRoute>
                <AssessmentAttempt />
              </ProtectedRoute>
            }
          />

          <Route
            path="/result/:attemptId"
            element={
              <ProtectedRoute>
                <AssessmentResult />
              </ProtectedRoute>
            }
          />

          {/* Competency */}

          <Route
            path="/competency"
            element={
              <ProtectedRoute>
                <Competency />
              </ProtectedRoute>
            }
          />

          {/* Roadmap */}

          <Route
            path="/roadmap"
            element={
              <ProtectedRoute>
                <Roadmap />
              </ProtectedRoute>
            }
          />

          {/* Resume */}

          <Route
            path="/resume"
            element={
              <ProtectedRoute>
                <Resume />
              </ProtectedRoute>
            }
          />

          {/* 404 */}

          <Route
            path="*"
            element={<Navigate to="/" replace />}
          />
          <Route
    path="/placement-readiness"
    element={<PlacementReadiness />}
/>

        </Routes>

      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
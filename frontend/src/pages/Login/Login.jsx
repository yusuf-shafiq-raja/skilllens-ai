import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

function Login() {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-blue-50 to-cyan-100 flex items-center justify-center p-6">

      <Card className="w-full max-w-md shadow-2xl rounded-2xl">

        <div className="flex flex-col items-center">

          <img
            src="/logo-dark.png"
            alt="SkillLens AI"
            className="w-24 h-24 object-contain mb-3"
          />

          <h1 className="text-4xl font-bold text-blue-600">
            SkillLens AI
          </h1>

          <p className="text-center text-slate-500 mt-2">
            AI-Powered Competency Intelligence Platform
          </p>

        </div>

        <form
          onSubmit={handleLogin}
          className="mt-8 space-y-5"
        >

          <Input
            label="Email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <div className="text-red-600 text-sm">
              {error}
            </div>
          )}

          <Button
            type="submit"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Login"}
          </Button>

        </form>

        <div className="mt-8 text-center">

          <p className="text-xs text-slate-400">
            © 2026 SkillLens AI
          </p>

        </div>

      </Card>

    </div>
  );
}

export default Login;
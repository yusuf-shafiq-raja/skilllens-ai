import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";
import Logo from "../../components/Logo/Logo";

function Login() {

  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const handleLogin = async (e) => {

    e.preventDefault();

    setError("");

    setLoading(true);

    try {

      await login(email, password);

      navigate("/dashboard");

    } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Login failed."
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">

      <Card className="w-full max-w-md">

        <Logo />

        <form
          onSubmit={handleLogin}
          className="mt-8 space-y-5"
        >

          <Input
            label="Email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          {

            error && (

              <div className="text-red-600 text-sm">

                {error}

              </div>

            )

          }

          <Button
            type="submit"
            disabled={loading}
          >

            {

              loading
                ? "Signing In..."
                : "Login"

            }

          </Button>

        </form>

      </Card>

    </div>

  );

}

export default Login;
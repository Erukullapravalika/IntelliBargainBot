import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Login({ setUser }) {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // ==============================
  // LOGIN
  // ==============================
  const handleLogin = async () => {

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {

      setLoading(true);

      const res = await fetch(
        "http://localhost:5000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email,
            password
          })
        }
      );

      const data = await res.json();

      setLoading(false);

      // ==============================
      // INVALID LOGIN
      // ==============================
      if (!res.ok) {

        alert(data.error || "Invalid credentials");

        return;
      }

      // ==============================
      // USER DATA
      // ==============================
      const userData = {
        id: data.user_id,
        name: data.name,
        email: data.email
      };

      // ==============================
      // STORE SESSION
      // ==============================
      localStorage.setItem(
        "user_id",
        data.user_id
      );

      localStorage.setItem(
        "sb_user",
        JSON.stringify(userData)
      );

      // ==============================
      // UPDATE STATE
      // ==============================
      setUser(userData);

      // ==============================
      // NAVIGATE
      // ==============================
      navigate("/products");

    } catch (err) {

      console.log(err);

      setLoading(false);

      alert("Server error. Please try again.");
    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-400 px-4">

      <div className="w-full max-w-md p-8 rounded-2xl bg-gray-900 border border-gray-300 shadow-lg">

        {/* TITLE */}
        <div className="text-center mb-8">

          <p className="text-blue-400 text-sm uppercase tracking-widest">
            IntelliBargainBot
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white">
            Welcome Back
          </h2>

          <p className="mt-2 text-gray-400 text-sm">
            Login to continue your smart shopping experience.
          </p>

        </div>

        {/* FORM */}
        <div className="space-y-5">

          {/* EMAIL */}
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="
              w-full px-4 py-3 rounded-lg
              bg-gray-800 text-white
              border border-gray-700
              focus:outline-none
              focus:border-blue-500
            "
          />

          {/* PASSWORD */}
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="
              w-full px-4 py-3 rounded-lg
              bg-gray-800 text-white
              border border-gray-700
              focus:outline-none
              focus:border-blue-500
            "
          />

          {/* BUTTON */}
          <button
            onClick={handleLogin}
            disabled={loading}
            className="
              w-full py-3 rounded-lg
              bg-gradient-to-r
              from-blue-500 to-indigo-600
              text-white font-medium
              hover:scale-[1.02]
              transition duration-300
            "
          >
            {
              loading
                ? "Logging in..."
                : "Login"
            }
          </button>

        </div>

        {/* SIGNUP */}
        <p className="text-center text-gray-400 text-sm mt-6">

          Don&apos;t have an account?{" "}

          <Link
            to="/signup"
            className="text-blue-400 hover:underline"
          >
            Sign Up
          </Link>

        </p>

      </div>

    </div>
  );
}
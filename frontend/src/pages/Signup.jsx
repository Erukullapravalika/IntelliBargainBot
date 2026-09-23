import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Signup({ onSignup }) {

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // ==============================
  // SIGNUP
  // ==============================
  const submit = async (e) => {

    e.preventDefault();

    if (!name || !email || !password) {
      alert("Please enter all fields");
      return;
    }

    try {

      setLoading(true);

      const res = await fetch(
        "http://127.0.0.1:5000/signup",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name,
            email,
            password
          })
        }
      );

      const data = await res.json();

      setLoading(false);

      // ==============================
      // ERROR
      // ==============================
      if (!res.ok) {

        alert(data.error || "Signup failed");

        return;
      }

      // ==============================
      // SUCCESS
      // ==============================
      const user = {
        id: data.user_id,
        name,
        email
      };

      // save local user
      localStorage.setItem(
        "sb_user",
        JSON.stringify(user)
      );

      localStorage.setItem(
        "user_id",
        data.user_id
      );

      // optional app state update
      if (onSignup) {
        onSignup(user);
      }

      alert("Account created successfully!");

      navigate("/products");

    } catch (err) {

      console.log(err);

      setLoading(false);

      alert("Server error. Please try again.");
    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">

      <div className="w-full max-w-md p-8 rounded-2xl bg-gray-900 border border-gray-300 shadow-2xl">

        {/* TITLE */}
        <div className="text-center mb-8">

          <p className="text-blue-400 text-sm uppercase tracking-widest">
            IntelliBargainBot
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white">
            Create Account
          </h2>

          <p className="mt-2 text-gray-400 text-sm">
            Start shopping and unlock smarter deals.
          </p>

        </div>

        {/* FORM */}
        <form
          className="space-y-5"
          onSubmit={submit}
        >

          {/* NAME */}
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            className="
              w-full px-4 py-3 rounded-lg
              bg-gray-800 text-white
              border border-gray-700
              focus:outline-none
              focus:border-blue-500
            "
          />

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
            type="submit"
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
                ? "Creating Account..."
                : "Sign Up"
            }
          </button>

        </form>

        {/* LOGIN */}
        <p className="text-center text-gray-400 text-sm mt-6">

          Already have an account?{" "}

          <Link
            to="/login"
            className="text-blue-400 hover:underline"
          >
            Login
          </Link>

        </p>

      </div>

    </div>
  );
}
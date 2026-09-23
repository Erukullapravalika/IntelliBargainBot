import React from "react";
import { Link } from "react-router-dom";

export default function Header({ cartCount, user, onLogout }) {
  return (
    <header className="py-4 px-6 bg-blue-600 shadow">
      <div className="container mx-auto flex justify-between items-center">
        
        {/* Logo */}
        <Link to="/" className="text-white font-bold text-xl">
          ShopNEX
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-6 text-white">
          <Link to="/">Home</Link>
          <Link to="/products">Shop</Link>

          <Link to="/cart">
            Cart
            <span className="ml-2 bg-white text-blue-600 rounded-full px-2 text-xs">
              {cartCount}
            </span>
          </Link>

          {/* Auth Links */}
          {!user ? (
            <>
              
              <Link to="/signup">Sign Up</Link>
            </>
          ) : (
            <button onClick={onLogout} className="font-medium">
              Logout
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}


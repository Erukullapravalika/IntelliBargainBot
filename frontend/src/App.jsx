import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Home from "./pages/Home";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Products from "./pages/Products";
import CartPage from "./pages/CartPage";
import ChatbotModal from "./components/ChatbotModal";

import { PRODUCTS } from "./products";

export default function App() {

  const [cart, setCart] = useState([]);

  const [user, setUser] = useState(() =>
    JSON.parse(localStorage.getItem("sb_user") || "null")
  );

  const [activeBotProduct, setActiveBotProduct] =
    useState(null);

  // =============================
  // ADD TO CART
  // =============================
  const addToCart = (product) => {

    setCart((prev) => {

      const exists = prev.find(
        (p) => p.id === product.id
      );

      if (exists) {

        return prev.map((p) =>

          p.id === product.id
            ? { ...p, qty: p.qty + 1 }
            : p

        );

      }

      return [
        ...prev,
        {
          ...product,
          qty: 1
        }
      ];

    });

  };

  // =============================
  // DECREASE QUANTITY
  // =============================
  const decreaseQuantity = (id) => {

    setCart((prev) => {

      return prev
        .map((item) => {

          if (item.id === id) {

            return {
              ...item,
              qty: item.qty - 1
            };

          }

          return item;

        })
        .filter((item) => item.qty > 0);

    });

  };

  // =============================
  // REMOVE COMPLETELY
  // =============================
  const removeFromCart = (id) => {

    setCart((prev) =>
      prev.filter((item) => item.id !== id)
    );

  };

  // =============================
  // OPEN BARGAIN BOT
  // =============================
  const openBot = (product) => {

    if (!user) {

      alert("Please login to use bargain bot.");

      return;

    }

    if (!product?.id) return;

    if (
      !product.isBrand &&
      product.price < 1000
    ) {

      alert(
        "Bargain bot available only for premium or branded items."
      );

      return;

    }

    localStorage.setItem(
      "product_id",
      product.id
    );

    setActiveBotProduct(product);

  };

  return (

    <div className="min-h-screen">

      {/* HEADER */}
      <Header
        cartCount={
          cart.reduce(
            (sum, p) => sum + p.qty,
            0
          )
        }
        user={user}
        onLogout={() => {

          setUser(null);

          localStorage.removeItem("sb_user");
          localStorage.removeItem("user_id");
          localStorage.removeItem("product_id");
          localStorage.removeItem("quantity");

        }}
      />

      {/* ROUTES */}
      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        {/* SIGNUP */}
        <Route
          path="/signup"
          element={
            <Signup
              onSignup={(u) => {

                setUser(u);

                localStorage.setItem(
                  "sb_user",
                  JSON.stringify(u)
                );

                if (u?.id) {

                  localStorage.setItem(
                    "user_id",
                    u.id
                  );

                }

              }}
            />
          }
        />

        {/* LOGIN */}
        <Route
          path="/login"
          element={
            <Login
              setUser={(u) => {

                setUser(u);

                localStorage.setItem(
                  "sb_user",
                  JSON.stringify(u)
                );

                if (u?.id) {

                  localStorage.setItem(
                    "user_id",
                    u.id
                  );

                }

              }}
            />
          }
        />

        {/* PRODUCTS */}
        <Route
          path="/products"
          element={
            <Products
              products={PRODUCTS}
              cart={cart}
              onAdd={addToCart}
              onIncrease={addToCart}
              onDecrease={decreaseQuantity}
            />
          }
        />

        {/* CART */}
        <Route
          path="/cart"
          element={
            <CartPage
              items={cart}
              onIncrease={addToCart}
              onDecrease={decreaseQuantity}
              onRemove={removeFromCart}
              onBargain={openBot}
            />
          }
        />

      </Routes>

      {/* CHATBOT */}
      {activeBotProduct && (

        <ChatbotModal
          product={activeBotProduct}
          onClose={() =>
            setActiveBotProduct(null)
          }
        />

      )}

      {/* FOOTER */}
      <footer className="py-6 text-center text-sm text-gray-300">

        © IntelliBargainBot

      </footer>

    </div>

  );

}
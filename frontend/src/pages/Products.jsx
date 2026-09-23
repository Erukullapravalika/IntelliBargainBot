// src/pages/Products.jsx
import React from "react";

export default function Products({
  products,
  cart,
  onAdd,
  onIncrease,
  onDecrease
}) {

  // =========================
  // GET QUANTITY
  // =========================
  const getQty = (id) => {
    const item = cart.find((p) => p.id === id);
    return item ? item.qty : 0;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 p-8">

      <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
        🛍 Explore Our Products
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">

        {products.map((product) => {

          const qty = getQty(product.id);

          return (
            <div
              key={product.id}
              className="bg-white rounded-xl shadow-md hover:shadow-xl transition p-4 flex flex-col"
            >

              {/* PRODUCT IMAGE */}
              <img
                src={product.image}
                alt={product.title}
                className="h-44 object-contain mb-3"
              />

              {/* TITLE */}
              <h2 className="font-semibold text-gray-800 text-sm mb-1 line-clamp-2">
                {product.title}
              </h2>

              {/* PRICE */}
              <p className="text-gray-700 font-medium mb-4">
                ₹{product.price}
              </p>

              {/* =========================
                  ADD TO CART / QUANTITY
              ========================== */}
              {qty === 0 ? (

                <button
                  onClick={() => {
                    localStorage.setItem("product_id", product.id);
                    onAdd(product);
                  }}
                  className="mt-auto bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Add to Cart
                </button>

              ) : (

                <div className="mt-auto flex items-center justify-between bg-gray-100 rounded-lg p-2">

                  {/* DECREASE */}
                  <button
                    onClick={() => onDecrease(product.id)}
                    className="w-10 h-10 rounded-lg bg-red-500 text-white text-xl hover:bg-red-600"
                  >
                    -
                  </button>

                  {/* QUANTITY */}
                  <span className="font-semibold text-lg text-gray-800">
                    {qty}
                  </span>

                  {/* INCREASE */}
                  <button
                    onClick={() => onIncrease(product)}
                    className="w-10 h-10 rounded-lg bg-green-500 text-white text-xl hover:bg-green-600"
                  >
                    +
                  </button>

                </div>

              )}

            </div>
          );
        })}

      </div>
    </div>
  );
}
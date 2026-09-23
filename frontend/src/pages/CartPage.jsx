import React from "react";

export default function CartPage({
  items,
  onIncrease,
  onDecrease,
  onRemove,
  onBargain
}) {

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-black p-8 text-white">

      <h2 className="text-3xl font-bold mb-8 text-black" >
        Your Cart
      </h2>

      {items.length === 0 && (
        <p className="text-black">
          Your cart is empty.
        </p>
      )}

      {items.map((item) => (

        <div
          key={item.id}
          className="flex flex-col md:flex-row md:items-center md:justify-between bg-gray-800 rounded-xl p-5 mb-5"
        >

          {/* PRODUCT INFO */}
          <div>

            <h3 className="font-semibold text-lg">
              {item.title}
            </h3>

            <p className="text-gray-300 mt-1">
              ₹{item.price}
            </p>

            {/* QUANTITY */}
            <div className="flex items-center gap-3 mt-3">

              <button
                onClick={() => onDecrease(item.id)}
                className="w-8 h-8 rounded bg-red-500 hover:bg-red-600"
              >
                -
              </button>

              <span className="font-semibold text-lg">
                {item.qty}
              </span>

              <button
                onClick={() => onIncrease(item)}
                className="w-8 h-8 rounded bg-green-500 hover:bg-green-600"
              >
                +
              </button>

            </div>

            {/* TOTAL */}
            <p className="text-cyan-300 mt-2">
              Total: ₹{item.price * item.qty}
            </p>

          </div>

          {/* ACTION BUTTONS */}
          <div className="flex gap-3 mt-5 md:mt-0">

            {item.isBrand && (
              <button
                onClick={() => {

                  localStorage.setItem(
                    "product_id",
                    item.id
                  );

                  localStorage.setItem(
                    "quantity",
                    item.qty
                  );

                  onBargain(item);

                }}
                className="bg-green-600 px-4 py-2 rounded hover:bg-green-700"
              >
                💬 Bargain
              </button>
            )}

            <button
              onClick={() => onRemove(item.id)}
              className="bg-red-600 px-4 py-2 rounded hover:bg-red-700"
            >
              Remove
            </button>

          </div>

        </div>

      ))}

    </div>
  );
}
import { useState } from "react";

export default function Chatbot({ product, onClose }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! You can bargain for this product 😊" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { from: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const user_id = localStorage.getItem("user_id");
      const product_id = localStorage.getItem("product_id");

      const res = await fetch("http://127.0.0.1:5000/negotiate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id,
          product_id,
          message: input
        })
      });

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { from: "bot", text: data.response }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { from: "bot", text: "⚠️ Server error. Please try again." }
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="fixed bottom-6 right-6 w-[90vw] max-w-[550px] h-[75vh] bg-gray-900 text-white rounded-2xl shadow-2xl flex flex-col z-50 border border-gray-700">


      {/* Header */}
      <div className="flex justify-between items-center px-4 py-3 bg-gray-800 rounded-t-2xl border-b border-gray-700">
        <h3 className="text-lg font-semibold">
          🤖 Smart Bargain Bot
        </h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white text-xl"
        >
          ✖
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.from === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2 rounded-xl max-w-[75%] text-sm shadow ${
                m.from === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-gray-300 text-black rounded-bl-none"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-sm text-gray-400">Bot is typing...</div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-800 flex gap-3 rounded-b-2xl border-t border-gray-700">
        <input
          className="flex-1 px-4 py-2 rounded-lg bg-white text-black text-sm focus:outline-none"
          placeholder="Type your offer (e.g. 800)…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-lg font-medium transition"
        >
          Send
        </button>
      </div>

    </div>
  );
}
import { useState, useEffect, useRef } from "react";

export default function ChatbotModal({ product, onClose }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // Scroll to bottom
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    setMessages([
      { from: "bot", text: `Hi 👋 Let's negotiate for "${product.title}"` }
    ]);
    localStorage.setItem("product_id", product.id);

    // RESET SESSION on bot open
    const user_id = localStorage.getItem("user_id");
    fetch("http://127.0.0.1:5000/reset_session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id,
        product_id: product.id
      })
    });

  }, [product]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const send = async () => {
    if (!input.trim()) return;

    const userMsg = input;

    setMessages(prev => [...prev, { from: "user", text: userMsg }]);
    setInput("");
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
          message: userMsg
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
        { from: "bot", text: "ss Something went wrong. Try again." }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="fixed bottom-6 right-6 w-[420px] h-[560px] backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl shadow-2xl flex flex-col z-50">

      {/* HEADER */}
      <div className="flex items-center justify-between px-4 py-3 bg-white/10 backdrop-blur-md rounded-t-2xl border-b border-white/20">
        <div>
          <h3 className="text-white font-semibold text-lg">
            🤖 Smart Bargain Bot
          </h3>
          <p className="text-xs text-gray-300">
            {product.title}
          </p>
        </div>

        <button
          onClick={onClose}
          className="text-gray-300 hover:text-white text-xl"
        >
          ✖
        </button>
      </div>

      {/* CHAT AREA */}
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
                  : "bg-white/80 text-black rounded-bl-none"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}

        {/* Typing animation */}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white/80 text-black px-4 py-2 rounded-xl text-sm flex gap-1">
              <span className="animate-bounce">•</span>
              <span className="animate-bounce delay-100">•</span>
              <span className="animate-bounce delay-200">•</span>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* INPUT */}
      <div className="p-4 flex gap-3 border-t border-white/20 bg-white/10 backdrop-blur-md rounded-b-2xl">
        <input
        className="flex-1 px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow"
        placeholder="Type your offer (e.g. 800)…"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        />

        <button
          onClick={send}
          className="px-5 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium shadow transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}
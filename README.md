# SmartBargainBot — Multi-page Tailwind + React (Vite) Demo

This project contains separate routes/pages for:
- Home (title + 3 feature cards)
- Signup (separate page)
- Products (product grid)
- Cart (cart page)

How to run:
1. Install Node.js (v18+ recommended).
2. In project folder:
   - npm install
   - npm run dev
3. Open the URL Vite shows (usually http://localhost:5173)

Notes:
- Tailwind version pinned to 3.4.13 to avoid registry version issues.
- The chatbot uses a mock API inside `src/components/ChatbotModal.jsx`. Replace it with your backend later.
- Modify `src/products.js` to add/change products.

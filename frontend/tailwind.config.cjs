/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primaryStart: '#6b46ff',
        primaryEnd: '#0ea5e9',
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          800: '#1e2a4a',
          900: '#0f172a',
        }
      }
    },
  },
  plugins: []
}
/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./src/**/*.{html,js,jsx}",
      'index.html',
      ],
  theme: {
    extend: {
      borderWidth:{
        '20': '20%',
      }
    },
  },
  plugins: [],
}


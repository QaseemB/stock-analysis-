/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./src/**/*.{html,js,jsx}",
      'index.html',
      ],
  theme: {
    extend: {
     colors: {
      background: '#6C6C6C',
      panel: '#1E1E1E',
      primary: '#2C3E55',
      success: '#22C55E',
      danger: '#EF4444',
      textPrimary: '#E5E7EB',
      textSecondary: '#9CA3AF',
      border: '#E5E7EB',
      hover: '#E0E7FF',
    },
      borderWidth:{
        '20': '20%',
      }
    },
  },
  plugins: [],
}


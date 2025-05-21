/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./src/**/*.{html,js,jsx}",
      'index.html',
      ],
  theme: {
    extend: {
     colors: {
      background: '#2C3E55',
      panel: '#DEDEDE',
      primary: '#6C6C6C',
      success: '#22C55E',
      danger: '#EF4444',
      textPrimary: '#E5E7EB',
      textSecondary: '#9CA3AF',
      border: '#212E49',
      hover: '#E0E7FF',
    },
      borderWidth:{
        '20': '20%',
      }
    },
  },
  plugins: [],
}


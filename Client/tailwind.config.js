/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./src/**/*.{html,js,jsx}",
      'index.html',
      ],
  theme: {
    extend: {
     colors: {
      background: '#F5F7FA',
      panel: '#FFFFFF',
      primary: '#1A73E8',
      success: '#22C55E',
      danger: '#EF4444',
      textPrimary: '#1F2937',
      textSecondary: '#6B7280',
      border: '#D1D5DB',
      hover: '#E0E7FF',
      accent: '#D9A441',
    },
      borderWidth:{
        '20': '20%',
      }
    },
  },
  plugins: [],
}


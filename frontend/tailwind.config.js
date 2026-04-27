/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        intimar: {
          primary: '#00938F',    // Teal/Turquesa principal
          bordeaux: '#B70050',   // Pantone 215C
          red: '#C41230',        // Pantone 187C
          orange: '#E36F1E',     // Pantone 159C
          gold: '#E7A614',       // Pantone 131C
          green: '#008A5E',      // Pantone 3415C
          dark: '#004D4B',       // Versión oscura del teal
        }
      },
      fontFamily: {
        sans: ['Inter', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Orange & White Theme
        primary: {
          DEFAULT: '#FF6B35',
          dark: '#E85D25',
          light: '#FFB088',
          pale: '#FFF4EF',
          50: '#FFF4EF',
          100: '#FFE4D6',
          200: '#FFCAAD',
          300: '#FFB088',
          400: '#FF8B5C',
          500: '#FF6B35',
          600: '#E85D25',
          700: '#C74D1A',
          800: '#A03E14',
          900: '#7A2F0F',
        },
        neutral: {
          white: '#FFFFFF',
          offWhite: '#FAFAFA',
          lightGray: '#F5F5F5',
          gray: '#E5E5E5',
          darkGray: '#718096',
          darker: '#2D3748',
        },
        success: {
          DEFAULT: '#38A169',
          light: '#68D391',
          dark: '#2F855A',
        },
        error: {
          DEFAULT: '#E53E3E',
          light: '#FC8181',
          dark: '#C53030',
        },
        warning: {
          DEFAULT: '#ED8936',
          light: '#F6AD55',
          dark: '#DD6B20',
        },
        info: {
          DEFAULT: '#3182CE',
          light: '#63B3ED',
          dark: '#2C5282',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },
      boxShadow: {
        'orange-glow': '0 0 20px rgba(255, 107, 53, 0.3)',
        'card': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'card-hover': '0 4px 16px rgba(255, 107, 53, 0.2)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-orange': 'pulseOrange 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseOrange: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}

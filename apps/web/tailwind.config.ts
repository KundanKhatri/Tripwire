import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#06070d",
          900: "#0a0c16",
          800: "#11141f",
          700: "#1a1e2d",
          600: "#262b3d",
        },
        accent: {
          DEFAULT: "#5b8cff",
          glow: "#7aa2ff",
        },
        block: "#ff5470",
        review: "#ffb454",
        allow: "#3ddc97",
      },
      fontFamily: {
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 40px -10px rgba(91,140,255,0.45)",
      },
    },
  },
  plugins: [],
};

export default config;

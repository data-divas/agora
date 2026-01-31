import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        agora: {
          dark: "#13714C",
          medium: "#3AB67D",
          light: "#A2E494",
          surface: "#E9EBED",
        },
      },
    },
  },
  plugins: [],
};

export default config;

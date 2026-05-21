import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./src/test-setup.js",
    globals: true,
    include: ["src/**/*.test.jsx"],
    exclude: ["backend/**", "dist/**", "node_modules/**"]
  }
});

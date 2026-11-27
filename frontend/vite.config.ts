import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    tsconfigPaths: true,
  },
  server: {
    proxy: {
      "/api": { target: process.env.API_PROXY_TARGET ?? "http://localhost:8000", changeOrigin: true },
    },
    watch: { usePolling: process.env.WATCHFILES_FORCE_POLLING === "true" },
  },
});

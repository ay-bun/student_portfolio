import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import legacy from "@vitejs/plugin-legacy";
import vue2 from "@vitejs/plugin-vue2";
import vue from "@vitejs/plugin-vue2";
import vue2Jsx from "@vitejs/plugin-vue2-jsx";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    // vue(), //new here
    vue2(),
    vue2Jsx(),
    legacy({
      targets: ["ie >= 11"],
      additionalLegacyPolyfills: ["regenerator-runtime/runtime"],
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
    extensions: [
      ".mjs",
      ".js",
      ".ts",
      ".jsx",
      ".tsx",
      ".json",
      ".vue",
      ".scss",
    ],
  },
  // server: {
  //   port: 3000,
  //   https: false,
  //   hmr: {
  //       host: "localhost",
  //       port: 3000,
  //       protocol: "wss",
  //   }
  // },
});

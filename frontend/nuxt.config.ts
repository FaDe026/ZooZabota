// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  vite: { plugins: [tailwindcss()] },
  css: ["./app/assets/css/main.css"],
  modules: ["@nuxtjs/google-fonts", "@nuxt/icon"],
  googleFonts: {
    families: {
      Cuprum: true,
    },
  },
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  icon: {
    mode: "svg",
    cssLayer: "base",
  },
  runtimeConfig: {
    public: {
      apiBase: "http://localhost:8000"
    }
  }
});

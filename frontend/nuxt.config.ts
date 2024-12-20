export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  components: true,
  app: {
    head: {
      title: 'IR',
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0, viewport-fit=cover',
      meta: [
        { name: 'color-scheme', content: 'light dark' },
      ],
    }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: 'http://localhost:8000'
    }
  },
  modules: [
    "@nuxtjs/google-fonts", 
    "@pinia/nuxt", 
  ],
  css: [
    '/styles/normalize.css',
    '/styles/global.css'
  ],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  googleFonts: {
    families: {
      'Raleway': true,
      'Oswald': true,
      'Quicksand': true,
    }
  }
})

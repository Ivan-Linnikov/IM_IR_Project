export default {
  content: [
    "./app.vue",
    "./pages/**/*.vue",
    "./components/**/*.vue",
    "./layouts/**/*.vue",
    "./plugins/**/*.js",
    "./nuxt.config.{js,ts}"
  ],
  theme: {
    extend: {
      fontFamily: {
        raleway: ['Raleway', 'sans-serif'],
        oswald: ['Oswald', 'sans-serif'],
        quicksand: ['Quicksand', 'sans-serif'],
      },
    },
  },
};
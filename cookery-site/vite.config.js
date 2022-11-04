import { fileURLToPath } from 'url'
import { defineConfig } from 'vite'
import { createVuePlugin as vue2 } from 'vite-plugin-vue2'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue2({
      jsx: true,
    }),
  ],
  resolve: {
    alias: {
      vue: 'vue/dist/vue.esm.js',
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'src': fileURLToPath(new URL('./src', import.meta.url)),
      'components': fileURLToPath(new URL('./src/components', import.meta.url)),
      'assets': fileURLToPath(new URL('./src/assets', import.meta.url)),
      // required for sass imports (since tilde is not supported out-of-the-box)
      '~bootstrap': 'bootstrap',
      '~bootstrap-vue': 'bootstrap-vue'
    },
  }
})
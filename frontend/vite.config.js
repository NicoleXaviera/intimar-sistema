import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'
import Icons from 'unplugin-icons/vite'
import Components from 'unplugin-vue-components/vite'
import IconsResolver from 'unplugin-icons/resolver'
import path from 'path'

export default defineConfig({
  define: {
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
  },
  plugins: [
    vue(),
    Components({
      resolvers: [
        IconsResolver({
          prefix: 'icon',
          enabledCollections: ['lucide'],
        }),
      ],
    }),
    Icons({
      compiler: 'vue3',
      autoInstall: true,
    }),
    frappeui({
      // Aquí forzamos la URL de tu backend
      frappeProxy: 'http://intimar.localhost:8000',
      lucideIcons: true,
      jinjaBootData: true,
      buildConfig: {
        indexHtmlPath: `../${getAppName()}/www/intimar.html`,
      },
    }),
  ],
  server: {
    allowedHosts: true,
    port: 8080,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  optimizeDeps: {
    exclude: ['frappe-ui'],
    include: [
      'feather-icons',
      'showdown',
    ],
  },
  build: {
    rollupOptions: {
      external: [
        /^~icons\//,
      ],
    },
  },
})

function getAppName() {
  return path.basename(path.resolve(__dirname, '..'))
}

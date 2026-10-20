import { resolve } from 'node:path'
import { defineConfig } from 'vite'

// Tres páginas: la landing (/), el login (/acceso/) y la página de la cuenta (/inicio/). El formulario vive en
// public/experiencia/ y Vite lo sirve tal cual: es JS vanilla que no pasa por el build.
//
// `strictPort`: si 5173 está ocupado, FALLA en vez de moverse solo, para que la URL sea siempre la misma.
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        acceso: resolve(import.meta.dirname, 'acceso/index.html'),
        inicio: resolve(import.meta.dirname, 'inicio/index.html'),
      },
    },
  },
  server: {
    port: process.env.PORT ? Number(process.env.PORT) : 5173,
    strictPort: true,
    // Las cuentas van contra el backend local con la misma ruta que en producción (vercel.json las reescribe a
    // Render), para que la cookie de sesión sea del mismo sitio. LEADIFY_API_LOCAL cambia el destino.
    proxy: {
      '^/api/(cuentas|sesion)(/.*)?$': {
        target: process.env.LEADIFY_API_LOCAL || 'http://127.0.0.1:8100',
        changeOrigin: false,
      },
    },
  },
})

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static',  // Huvudkatalog för byggda filer
    assetsDir: 'assets',  // Undermapp för tillgångar
  },
  base: '/static/',  // Bas-URL för alla resurser
})
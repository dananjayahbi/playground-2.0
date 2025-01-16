import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()], // Enable React JSX handling
  base: './', // Use relative paths for assets to work in portable builds
  build: {
    outDir: 'dist', // Output directory for build files
    rollupOptions: {
      // Ensure entry point compatibility for Electron
      input: './index.html',
    },
  },
  server: {
    port: 4173, // Dev server port (optional)
    strictPort: true, // Fail if port 4173 is unavailable
  },
});

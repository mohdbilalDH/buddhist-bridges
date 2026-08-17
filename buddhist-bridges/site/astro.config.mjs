import { defineConfig } from 'astro/config';

// Local dev serves from '/'. CI sets ASTRO_BASE=/<repo-name> and
// ASTRO_SITE=https://<owner>.github.io for the GitHub Pages deploy.
export default defineConfig({
  output: 'static',
  site: process.env.ASTRO_SITE,
  base: process.env.ASTRO_BASE || '/',
  trailingSlash: 'ignore',
});

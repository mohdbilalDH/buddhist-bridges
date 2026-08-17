// Copy the outputs/web contract into the site (never symlink — dh-site-publish rule).
import { cpSync, mkdirSync } from 'node:fs';
const src = new URL('../outputs/web/', import.meta.url);
for (const dest of ['./public/data/', './src/data/']) {
  mkdirSync(new URL(dest, import.meta.url), { recursive: true });
  cpSync(src, new URL(dest, import.meta.url), { recursive: true });
}
console.log('synced outputs/web -> site/public/data + site/src/data');

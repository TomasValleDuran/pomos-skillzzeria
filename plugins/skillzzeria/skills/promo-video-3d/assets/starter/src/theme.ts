import { loadFont as loadDisplay } from '@remotion/google-fonts/InterTight';
import { loadFont as loadText } from '@remotion/google-fonts/Inter';

// Replace with the product's tokens (read its design system / globals.css). One accent, rationed.
export const C = {
  bg: '#000000',
  accent: '#4ea8ff',
  accentInk: '#001226', // text on accent fills
  accentGlow: 'rgba(78,168,255,.45)',
  ink100: '#ffffff',
  ink80: 'rgba(255,255,255,.80)',
  ink64: 'rgba(255,255,255,.64)',
};

export const DISPLAY = loadDisplay('normal', { weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext'] }).fontFamily;
export const TEXT = loadText('normal', { weights: ['400', '500', '600'], subsets: ['latin', 'latin-ext'] }).fontFamily;

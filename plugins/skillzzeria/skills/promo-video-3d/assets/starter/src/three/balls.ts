import * as THREE from 'three';

// Equirectangular sport-ball textures generated in code (no third-party assets). Use on a sphereGeometry.
const W = 1024;
const H = 512;

const paint = (fn: (n: THREE.Vector3, lon: number, lat: number) => [number, number, number]) => {
  const c = document.createElement('canvas');
  c.width = W;
  c.height = H;
  const ctx = c.getContext('2d')!;
  const img = ctx.createImageData(W, H);
  const n = new THREE.Vector3();
  for (let y = 0; y < H; y++) {
    const lat = Math.PI / 2 - (y / H) * Math.PI;
    for (let x = 0; x < W; x++) {
      const lon = (x / W) * Math.PI * 2 - Math.PI;
      n.set(Math.cos(lat) * Math.sin(lon), Math.sin(lat), Math.cos(lat) * Math.cos(lon));
      const [r, g, b] = fn(n, lon, lat);
      const i = (y * W + x) * 4;
      img.data[i] = r;
      img.data[i + 1] = g;
      img.data[i + 2] = b;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
};

// Classic football: truncated icosahedron = Voronoi of 12 pentagons (icosahedron vertices)
// and 20 hexagons (vertices of the DUAL dodecahedron — the permutation below matters).
const phi = (1 + Math.sqrt(5)) / 2;
const ICO = [
  [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
  [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
  [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1],
].map(([x, y, z]) => new THREE.Vector3(x, y, z).normalize());
const DOD: THREE.Vector3[] = [];
for (const sx of [-1, 1]) for (const sy of [-1, 1]) for (const sz of [-1, 1]) DOD.push(new THREE.Vector3(sx, sy, sz).normalize());
for (const [a, b2] of [[1 / phi, phi]]) {
  for (const s1 of [-1, 1])
    for (const s2 of [-1, 1]) {
      DOD.push(new THREE.Vector3(0, s2 * b2, s1 * a).normalize());
      DOD.push(new THREE.Vector3(s1 * a, 0, s2 * b2).normalize());
      DOD.push(new THREE.Vector3(s2 * b2, s1 * a, 0).normalize());
    }
}
const CENTERS = [...ICO.map((v) => ({ v, penta: true })), ...DOD.map((v) => ({ v, penta: false }))];

export const footballTexture = () =>
  paint((n) => {
    let best = -2;
    let second = -2;
    let penta = false;
    for (const c of CENTERS) {
      const d = n.dot(c.v) - (c.penta ? 0.02 : 0);
      if (d > best) {
        second = best;
        best = d;
        penta = c.penta;
      } else if (d > second) second = d;
    }
    if (best - second < 0.012) return [40, 40, 44]; // seams
    return penta ? [18, 18, 22] : [244, 244, 240];
  });

export const basketballTexture = () =>
  paint((n) => {
    const line = 0.018;
    const grain = (Math.sin(n.x * 400) * Math.sin(n.y * 400) * Math.sin(n.z * 400)) * 10;
    const isLine =
      Math.abs(n.y) < line || Math.abs(n.x) < line || Math.abs(Math.abs(n.z) - 0.72 - 0.12 * n.y * n.y) < line;
    if (isLine) return [20, 12, 8];
    return [216 + grain, 104 + grain * 0.5, 36];
  });

const seamBall = (base: [number, number, number]) =>
  paint((n, lon, lat) => {
    const seam = 0.42 * Math.sin(2 * lon);
    const d = Math.abs(lat - seam);
    const fuzz = (Math.sin(lon * 900) * Math.cos(lat * 700)) * 8;
    if (d < 0.035) return [240, 240, 232];
    return [base[0] + fuzz, base[1] + fuzz, base[2]];
  });

export const tennisTexture = () => seamBall([206, 228, 70]);
export const padelTexture = () => seamBall([238, 226, 60]);

// Volleyball: three stripe groups per dominant axis, yellow / blue / white, with seams.
export const volleyTexture = () =>
  paint((n) => {
    const v = [n.x, n.y, n.z];
    const abs = v.map(Math.abs);
    const axis = abs.indexOf(Math.max(...abs));
    const sorted = [...abs].sort((a, b) => b - a);
    if (sorted[0] - sorted[1] < 0.025) return [40, 44, 60]; // border between groups
    const u = v[(axis + 1) % 3] / abs[axis]; // -1..1 within the group
    const stripe = Math.min(2, Math.floor((u + 1) * 1.5));
    const edge = Math.abs((u + 1) * 1.5 - Math.round((u + 1) * 1.5));
    if (edge < 0.04 && Math.abs(u) < 0.99) return [60, 64, 80];
    const palette: [number, number, number][][] = [
      [[255, 205, 40], [30, 90, 200], [245, 245, 240]],
      [[30, 90, 200], [245, 245, 240], [255, 205, 40]],
      [[245, 245, 240], [255, 205, 40], [30, 90, 200]],
    ];
    return palette[axis][stripe];
  });

// Rugby: white with stripes near the tips and lengthwise seams (stretch the sphere 1.55x on X).
export const rugbyTexture = () =>
  paint((n) => {
    const ax = Math.abs(n.x);
    const ang = Math.atan2(n.z, n.y);
    const seam = Math.abs(Math.sin(ang * 2)) < 0.03 && ax < 0.9;
    if (seam) return [70, 60, 50];
    if (ax > 0.55 && ax < 0.7) return [30, 90, 200];
    if (ax > 0.72 && ax < 0.78) return [220, 40, 60];
    const grain = Math.sin(n.y * 300) * Math.sin(n.z * 300) * 6;
    return [236 + grain, 230 + grain, 218 + grain];
  });

// Baseball: white with the red double-stitched seam.
export const baseballTexture = () =>
  paint((n, lon, lat) => {
    const seam = 0.42 * Math.sin(2 * lon);
    const d = lat - seam;
    const ad = Math.abs(d);
    if (ad > 0.025 && ad < 0.07 && Math.sin(lon * 90) > 0.2) return [200, 30, 40];
    if (ad < 0.012) return [215, 205, 195];
    return [245, 242, 232];
  });

// Golf: white with subtle dimple shading.
export const golfTexture = () =>
  paint((n, lon, lat) => {
    const a = Math.sin(lon * 60 * Math.cos(lat)) * Math.sin(lat * 60);
    const s = 238 - Math.max(0, a) * 28;
    return [s, s, s + 4];
  });

export const pingpongTexture = () => paint(() => [255, 128, 30]);

// Padel paddle: rounded perforated head + handle, extruded. Groups: material-0 faces, material-1 sides.
export const palaGeometry = () => {
  const s = new THREE.Shape();
  const w = 0.26; // half width of the head
  const top = 0.5;
  const neck = -0.14;
  s.moveTo(-0.045, -0.42);
  s.lineTo(-0.045, neck - 0.06);
  s.bezierCurveTo(-0.07, neck - 0.02, -w, neck + 0.02, -w, 0.16);
  s.bezierCurveTo(-w, 0.38, -0.16, top, 0, top);
  s.bezierCurveTo(0.16, top, w, 0.38, w, 0.16);
  s.bezierCurveTo(w, neck + 0.02, 0.07, neck - 0.02, 0.045, neck - 0.06);
  s.lineTo(0.045, -0.42);
  s.lineTo(-0.045, -0.42);
  // grid of holes inside the head
  for (let y = -0.02; y <= 0.4; y += 0.055)
    for (let x = -0.19; x <= 0.19; x += 0.055) {
      const cy = 0.16;
      if ((x / 0.2) ** 2 + ((y - cy) / 0.27) ** 2 > 0.85) continue;
      const h = new THREE.Path();
      h.absarc(x, y, 0.012, 0, Math.PI * 2, true);
      s.holes.push(h);
    }
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.035, bevelEnabled: true, bevelThickness: 0.008, bevelSize: 0.008, bevelSegments: 3, curveSegments: 24 });
  g.translate(0, 0, -0.0175);
  return g;
};

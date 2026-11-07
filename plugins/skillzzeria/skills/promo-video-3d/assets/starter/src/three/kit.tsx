// Shared 3D pieces: Stage (light + bloom), camera rig, mirrored floor, glows, textures, shapes, PRNG.
// Every animated value must be a pure function of useCurrentFrame() — Remotion renders frames out of order in parallel tabs.
import React, { useMemo, useState } from 'react';
import * as THREE from 'three';
import { ThreeCanvas } from '@remotion/three';
import { useThree, type ThreeElements } from '@react-three/fiber';
import { Environment, Lightformer, MeshReflectorMaterial } from '@react-three/drei';
import { Bloom, EffectComposer, Noise, Vignette } from '@react-three/postprocessing';
import { continueRender, delayRender, useCurrentFrame, useVideoConfig } from 'remotion';
import { C } from '../theme';
import { Warmup } from './Warmup';

export const ACCENT = C.accent;

// ---------- stage ----------
export const Stage: React.FC<{
  children: React.ReactNode;
  fov?: number;
  bloom?: number;
  threshold?: number;
  env?: number;
  fog?: [number, number]; // dissolves floors/horizons into black; ~2x and ~4x the camera distance
}> = ({ children, fov = 35, bloom = 1, threshold = 0.8, env = 0.5, fog }) => {
  const { width, height } = useVideoConfig();
  return (
    <ThreeCanvas width={width} height={height} camera={{ fov, position: [0, 0, 10], near: 0.05, far: 300 }} gl={{ antialias: true, preserveDrawingBuffer: true }}>
      <Warmup />
      <color attach="background" args={['#000']} />
      {fog && <fog attach="fog" args={['#000', fog[0], fog[1]]} />}
      <Environment resolution={256} environmentIntensity={env}>
        <Lightformer intensity={2} position={[0, 5, 3]} scale={[10, 2, 1]} />
        <Lightformer intensity={2.5} color={ACCENT} position={[-6, 1, 1]} rotation-y={Math.PI / 2} scale={[8, 3, 1]} />
        <Lightformer intensity={1.2} position={[6, 1, 1]} rotation-y={-Math.PI / 2} scale={[8, 3, 1]} />
      </Environment>
      {children}
      <EffectComposer multisampling={4}>
        <Bloom intensity={bloom} luminanceThreshold={threshold} luminanceSmoothing={0.25} mipmapBlur />
        <Vignette darkness={0.65} offset={0.25} />
        <Noise opacity={0.035} />
      </EffectComposer>
    </ThreeCanvas>
  );
};

// ---------- camera, set from props each frame ----------
export const Cam: React.FC<{ pos: number[]; look: number[]; fov?: number; shake?: number }> = ({ pos, look, fov, shake = 0 }) => {
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  const frame = useCurrentFrame();
  const sx = shake * (Math.sin(frame * 7.3) + Math.sin(frame * 13.1)) * 0.5;
  const sy = shake * (Math.cos(frame * 9.7) + Math.sin(frame * 5.3)) * 0.5;
  camera.position.set(pos[0] + sx, pos[1] + sy, pos[2]);
  camera.lookAt(look[0], look[1], look[2]);
  if (fov && camera.fov !== fov) {
    camera.fov = fov;
    camera.updateProjectionMatrix();
  }
  return null;
};

// ---------- mirrored floor: only in scenes where something touches it ----------
export const Floor: React.FC<{ y?: number; color?: string; mirror?: number }> = ({ y = 0, color = '#050608', mirror = 0.6 }) => (
  <mesh rotation-x={-Math.PI / 2} position-y={y}>
    <planeGeometry args={[200, 200]} />
    <MeshReflectorMaterial
      resolution={1024}
      blur={[400, 100]}
      mixBlur={1}
      mixStrength={4}
      mirror={mirror}
      roughness={0.85}
      depthScale={1}
      minDepthThreshold={0.4}
      maxDepthThreshold={1.4}
      color={color}
      metalness={0.6}
      envMapIntensity={0.12} // higher turns the floor into a grey band
    />
  </mesh>
);

// ---------- additive glow sprite ----------
let glowTex: THREE.Texture | null = null;
export const glowTexture = () => {
  if (glowTex) return glowTex;
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const ctx = c.getContext('2d')!;
  const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.2, 'rgba(255,255,255,.5)');
  g.addColorStop(0.5, 'rgba(255,255,255,.12)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 256, 256);
  glowTex = new THREE.CanvasTexture(c);
  return glowTex;
};

// depthTest={false} when the halo would cross a floor (otherwise it is clipped into a hard horizon line).
export const Glow: React.FC<{ color?: string; opacity?: number; scale?: number; depthTest?: boolean } & ThreeElements['sprite']> = ({
  color = ACCENT,
  opacity = 1,
  scale = 1,
  depthTest = true,
  ...s
}) => (
  <sprite {...s} scale={[scale, scale, 1]}>
    <spriteMaterial map={glowTexture()} color={color} transparent opacity={opacity} blending={THREE.AdditiveBlending} depthWrite={false} depthTest={depthTest} />
  </sprite>
);

// ---------- brand shapes: extrude a 2D polygon (e.g. logo pieces from the SVG) ----------
// points in SVG units; center/unit convert them to scene units. Thin bevel (≈5% of depth) — big bevels look like a frame.
export const extrudePolygon = (points: [number, number][], { center = [48, 48], unit = 36, depth = 0.22 } = {}) => {
  const s = new THREE.Shape();
  points.forEach(([x, y], i) => {
    const vx = (x - center[0]) / unit;
    const vy = -(y - center[1]) / unit;
    if (i === 0) s.moveTo(vx, vy);
    else s.lineTo(vx, vy);
  });
  s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.01, bevelSegments: 8 });
  g.translate(0, 0, -depth / 2);
  return g;
};

// Glossy brand material. Whites need emissive ~0.4 or they read grey under a single key light.
export const BrandMat: React.FC<{ color: string; glow?: number }> = ({ color, glow = 0 }) => (
  <meshPhysicalMaterial
    color={color}
    emissive={color}
    emissiveIntensity={(color.toLowerCase() === '#ffffff' ? 0.42 : 0.45) + glow}
    roughness={0.2}
    metalness={0.1}
    clearcoat={1}
  />
);

// ---------- textures that block the render until loaded ----------
export const useImageTexture = (src: string, setup?: (t: THREE.Texture) => void) => {
  const [handle] = useState(() => delayRender(`texture ${src}`));
  return useMemo(() => {
    const t = new THREE.TextureLoader().load(src, () => continueRender(handle), undefined, () => continueRender(handle));
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    setup?.(t);
    return t;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src]);
};

// Rounded rectangle with 0–1 UVs (phone screens).
export const roundedRect = (w: number, h: number, r: number) => {
  const s = new THREE.Shape();
  const x = -w / 2;
  const y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y);
  s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h);
  s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r);
  s.quadraticCurveTo(x, y, x + r, y);
  const g = new THREE.ShapeGeometry(s, 16);
  const pos = g.attributes.position;
  const uv = g.attributes.uv;
  for (let i = 0; i < pos.count; i++) uv.setXY(i, (pos.getX(i) + w / 2) / w, (pos.getY(i) + h / 2) / h);
  return g;
};

// Deterministic PRNG: the same frame must look identical in any render tab.
export const rand = (seed: number) => () => {
  seed |= 0;
  seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

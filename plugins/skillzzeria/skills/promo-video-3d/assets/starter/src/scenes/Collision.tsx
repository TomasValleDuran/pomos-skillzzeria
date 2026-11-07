// Example hero scene: two halves of a mark fly in and collide on beat 2 → flash, shockwaves, particle burst, wordmark.
// Replace HALVES with the product's logo pieces (polygons from its SVG).
import React, { useMemo } from 'react';
import * as THREE from 'three';
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { Slam } from '../components/Slam';
import { C, DISPLAY } from '../theme';
import { b } from '../timing';
import { ACCENT, BrandMat, Cam, extrudePolygon, Glow, glowTexture, rand, Stage } from '../three/kit';

const HIT = b(2);
const HALVES: { points: [number, number][]; color: string; from: number }[] = [
  { points: [[30, 30], [30, 66], [54, 48]], color: ACCENT, from: -1 },
  { points: [[66, 30], [66, 66], [42, 48]], color: '#ffffff', from: 1 },
];

const Burst: React.FC<{ t: number }> = ({ t }) => {
  const { geo, dirs } = useMemo(() => {
    const r = rand(3);
    const n = 900;
    const d = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const th = r() * Math.PI * 2;
      const z = (r() - 0.5) * 0.7;
      const s = 0.6 + r() * r() * 6;
      d[i * 3] = Math.cos(th) * Math.sqrt(1 - z * z) * s;
      d[i * 3 + 1] = Math.sin(th) * Math.sqrt(1 - z * z) * s * 0.75;
      d[i * 3 + 2] = z * s;
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    return { geo: g, dirs: d };
  }, []);
  if (t < 0) return null;
  const k = 1 - Math.exp(-t / 9);
  const pos = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < pos.count; i++) pos.setXYZ(i, dirs[i * 3] * k, dirs[i * 3 + 1] * k, dirs[i * 3 + 2] * k);
  pos.needsUpdate = true;
  return (
    <points geometry={geo}>
      <pointsMaterial map={glowTexture()} size={0.09} color="#cfe6ff" transparent opacity={interpolate(t, [0, 50], [1, 0], { extrapolateRight: 'clamp' })} blending={THREE.AdditiveBlending} depthWrite={false} />
    </points>
  );
};

const Ring: React.FC<{ t: number; delay?: number; color?: string }> = ({ t, delay = 0, color = '#ffffff' }) => {
  const tt = t - delay;
  if (tt < 0 || tt > 30) return null;
  return (
    <mesh scale={interpolate(tt, [0, 30], [0.2, 9], { easing: Easing.out(Easing.cubic) })}>
      <ringGeometry args={[0.92, 1, 128]} />
      <meshBasicMaterial color={color} transparent opacity={interpolate(tt, [0, 30], [0.9, 0])} blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
    </mesh>
  );
};

export const Collision: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const geos = useMemo(() => HALVES.map((h) => extrudePolygon(h.points)), []);
  const fly = interpolate(frame, [0, HIT], [1, 0], { extrapolateRight: 'clamp', easing: Easing.in(Easing.quad) });
  const t = frame - HIT;
  const settle = t >= 0 ? spring({ frame: t, fps, config: { damping: 9, stiffness: 180 } }) : 0;
  const glow = t >= 0 ? 2.2 * Math.exp(-t / 8) : 0.3;
  const word = interpolate(t, [14, 28], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill>
      <Stage bloom={1.2 + glow * 0.6} threshold={0.75} env={0.6} fog={[6, 13]}>
        <Cam pos={[0, 0.25, 5.6]} look={[0, 0.1, 0]} shake={t >= 0 && t < 12 ? 0.08 * (1 - t / 12) : 0} />
        <ambientLight intensity={0.2} />
        <directionalLight position={[2, 3, 5]} intensity={1.3} />
        <group position-y={t > 0 ? 0.4 * Math.min(1, t / 25) : 0} scale={t >= 0 ? interpolate(settle, [0, 1], [1.35, 1]) : 1}>
          {HALVES.map((h, i) => (
            // spin eased by fly² so the pieces arrive face-on
            <mesh key={i} geometry={geos[i]} position={[h.from * fly * 12, 0, (i ? 1 : -1) * 0.07]} rotation={[h.from * fly * fly * Math.PI * 4, 0, 0]}>
              <BrandMat color={h.color} glow={glow} />
            </mesh>
          ))}
        </group>
        <Ring t={t} />
        <Ring t={t} delay={4} color={ACCENT} />
        <Burst t={t} />
        <Glow color="#ffffff" scale={t >= 0 ? 1 + glow * 3 : 0.01} opacity={Math.min(1, glow)} />
        <Glow scale={10} opacity={t >= 0 ? 0.35 : 0} />
      </Stage>
      <AbsoluteFill style={{ background: '#fff', opacity: t >= 0 ? interpolate(t, [0, 1, 6], [0, 0.9, 0], { extrapolateRight: 'clamp' }) : 0 }} />
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'flex-end', paddingBottom: 170 }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 800, fontSize: 150, letterSpacing: '-0.035em', color: C.ink100, clipPath: `inset(-40% ${102 - word * 116}% -40% -8%)` }}>
          Brand
        </div>
      </AbsoluteFill>
      <Slam f={frame - b(10)} len={b(5)} size={150} bottom>
        Your call to action.
      </Slam>
    </AbsoluteFill>
  );
};

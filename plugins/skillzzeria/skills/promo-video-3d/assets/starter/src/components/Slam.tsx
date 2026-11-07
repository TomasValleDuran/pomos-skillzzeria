import React from 'react';
import { interpolate, spring, useVideoConfig } from 'remotion';
import { C, DISPLAY, TEXT } from '../theme';

// Text that "slams" on the beat: enters big and blurred, settles, exits fast. Lives in the 2D layer over the canvas.
export const Slam: React.FC<{
  f: number; // local frame (frame - start)
  len: number; // frames on screen
  children: React.ReactNode;
  size?: number;
  sub?: string;
  align?: 'center' | 'left';
  bottom?: boolean;
  style?: React.CSSProperties;
}> = ({ f, len, children, size = 170, sub, align = 'center', bottom = false, style }) => {
  const { fps } = useVideoConfig();
  if (f < 0 || f >= len) return null;
  const slam = spring({ frame: f, fps, config: { damping: 14, stiffness: 260, mass: 0.6 } });
  const out = interpolate(f, [len - 5, len], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const subIn = spring({ frame: f - 6, fps, config: { damping: 20, stiffness: 180 } });
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: bottom ? 'flex-end' : 'center',
        alignItems: align === 'center' ? 'center' : 'flex-start',
        padding: `0 0 ${bottom ? 120 : 0}px ${align === 'left' ? 150 : 0}px`,
        gap: 24,
        ...style,
      }}
    >
      <div
        style={{
          fontFamily: DISPLAY,
          fontWeight: 900,
          fontSize: size,
          lineHeight: 0.98,
          letterSpacing: '-0.045em',
          color: C.ink100,
          textAlign: align,
          transform: `scale(${interpolate(slam, [0, 1], [1.35, 1])}) translateY(${-out * 30}px)`,
          transformOrigin: align === 'left' ? 'left center' : 'center',
          filter: `blur(${(1 - slam) * 16 + out * 10}px)`,
          opacity: slam * (1 - out),
          textShadow: '0 8px 60px rgba(0,0,0,.75)',
        }}
      >
        {children}
      </div>
      {sub && (
        <div
          style={{
            fontFamily: TEXT,
            fontWeight: 500,
            fontSize: 38,
            color: C.ink80,
            opacity: subIn * (1 - out),
            transform: `translateY(${(1 - subIn) * 20}px)`,
            textShadow: '0 4px 30px rgba(0,0,0,.8)',
          }}
        >
          {sub}
        </div>
      )}
    </div>
  );
};

export const Accent: React.FC<{ children: React.ReactNode }> = ({ children }) => <span style={{ color: C.accent }}>{children}</span>;

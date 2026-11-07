import { useThree } from '@react-three/fiber';
import { useLayoutEffect } from 'react';
import { continueRender, delayRender } from 'remotion';

// EffectComposer (bloom) outputs pure black on the first frame each render tab draws.
// This forces a few render passes on mount, before Remotion captures the frame. Put it inside every ThreeCanvas.
export const Warmup: React.FC = () => {
  const advance = useThree((s) => s.advance);
  useLayoutEffect(() => {
    const handle = delayRender('warmup bloom');
    let n = 0;
    const tick = () => {
      advance(performance.now());
      if (++n < 3) requestAnimationFrame(tick);
      else continueRender(handle);
    };
    requestAnimationFrame(tick);
  }, [advance]);
  return null;
};

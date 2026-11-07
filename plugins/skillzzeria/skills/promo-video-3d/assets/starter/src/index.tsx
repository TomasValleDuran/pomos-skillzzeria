import React from 'react';
import { AbsoluteFill, Audio, Composition, registerRoot, Sequence, staticFile } from 'remotion';
import { Collision } from './scenes/Collision';
import { C } from './theme';
import { FPS, SCENES, TOTAL } from './timing';

// One <Sequence> per scene; each scene owns its <Stage>. Audio is one pre-mixed WAV in public/ (see the skill's audio reference).
// `audio` is a prop so stills can pass {"audio":null}.
const Main: React.FC<{ audio?: string | null }> = ({ audio = null }) => (
  <AbsoluteFill style={{ background: C.bg }}>
    {audio && <Audio src={staticFile(audio)} />}
    <Sequence from={SCENES.collision.from} durationInFrames={SCENES.collision.dur} name="Collision">
      <Collision />
    </Sequence>
  </AbsoluteFill>
);

const Root: React.FC = () => (
  <Composition id="Main" component={Main} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} defaultProps={{ audio: null }} />
);

registerRoot(Root);

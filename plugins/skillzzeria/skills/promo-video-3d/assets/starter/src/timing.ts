// Single source of timing. Everything (scenes, text slams, music, SFX) is placed in beats on this grid.
// Change BPM here if you swap in a real track; cuts move with it.
export const FPS = 30;
export const BPM = 120;
export const BEAT = (60 / BPM) * FPS; // 15 frames
export const BAR = BEAT * 4;

export const b = (beats: number) => Math.round(beats * BEAT);

// Scenes in beats. Keep the same numbers in the music arrangement.
export const SCENES = {
  collision: { from: 0, dur: b(16) },
};
export const TOTAL = SCENES.collision.from + SCENES.collision.dur;

// 1 on the beat, decaying to 0 before the next: drive glows/scales with the music.
export const beatPulse = (frame: number, every = 1) => {
  const period = BEAT * every;
  return Math.pow(1 - (frame % period) / period, 3);
};

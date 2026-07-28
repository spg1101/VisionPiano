import * as Tone from "tone";

// Maps chord name -> the notes to sound. Extend/adjust voicings as you like -
// these are simple close-position triads/7ths in one octave.
const CHORD_VOICINGS: Record<string, string[]> = {
  A: ["A3", "C#4", "E4"],
  Am: ["A3", "C4", "E4"],
  B: ["B3", "D#4", "F#4"],
  Bm: ["B3", "D4", "F#4"],
  C: ["C4", "E4", "G4"],
  D: ["D4", "F#4", "A4"],
  Dm: ["D4", "F4", "A4"],
  E: ["E3", "G#3", "B3"],
  Em: ["E3", "G3", "B3"],
  F: ["F3", "A3", "C4"],
  G: ["G3", "B3", "D4"],
  "F#m": ["F#3", "A3", "C#4"],
};

let sampler: Tone.Sampler | null = null;
let ready: Promise<void> | null = null;

/**
 * Loads real piano samples (not a synthesized oscillator) so chords actually
 * sound like a piano. Point the urls at your own hosted sample set, e.g. the
 * Salamander Grand Piano samples, placed under /public/piano-samples/.
 */
export function loadPiano(): Promise<void> {
  if (!ready) {
    sampler = new Tone.Sampler({
      urls: {
        C3: "C3.mp3",
        C4: "C4.mp3",
        C5: "C5.mp3",
      },
      baseUrl: "/piano-samples/",
      onload: () => {},
    }).toDestination();

    ready = new Promise((resolve) => {
      Tone.loaded().then(() => resolve());
    });
  }
  return ready;
}

export async function playChord(chordName: string, durationSeconds = 1.5) {
  await Tone.start(); // required: must run after a user gesture (a click/tap)
  await loadPiano();
  const notes = CHORD_VOICINGS[chordName];
  if (!notes) {
    console.warn(`No voicing defined for chord "${chordName}"`);
    return;
  }
  sampler!.triggerAttackRelease(notes, durationSeconds);
}

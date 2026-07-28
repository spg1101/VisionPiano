"use client";

import { useEffect, useRef } from "react";
import { playChord } from "../lib/tonePiano";

// TODO: replace with the chord progression for whatever song is loaded,
// pulled from the /songs/{artist}/{title} backend response. Gesture index
// (1-5) selects position in this list.
const DEMO_PROGRESSION = ["A", "F#m", "D", "E"];

function gestureToChord(gesture: string | null): string | null {
  if (!gesture) return null;
  const index = parseInt(gesture.split("_")[0], 10) - 1;
  return DEMO_PROGRESSION[index] ?? null;
}

export default function ChordSynth({ gesture }: { gesture: string | null }) {
  const lastPlayed = useRef<string | null>(null);

  useEffect(() => {
    const chord = gestureToChord(gesture);
    // Only re-trigger when the gesture actually changes, so holding a
    // gesture steady doesn't retrigger the chord every animation frame.
    if (chord && chord !== lastPlayed.current) {
      playChord(chord);
      lastPlayed.current = chord;
    } else if (!chord) {
      lastPlayed.current = null;
    }
  }, [gesture]);

  return <div>Current chord: {gestureToChord(gesture) ?? "—"}</div>;
}

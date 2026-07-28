"use client";

import { useState } from "react";
import ChordSynth from "../components/ChordSynth";
import GestureDetector from "../components/GestureDetector";
import LyricsDisplay from "../components/LyricsDisplay";
import AudioTranscriber from "../components/AudioTranscriber";

export default function Home() {
  const [currentGesture, setCurrentGesture] = useState<string | null>(null);
  const [transcript, setTranscript] = useState("");

  return (
    <main>
      <h1>chord-singer</h1>

      {/* Loads chord/lyric data for a song from the FastAPI backend, and
          renders the scrolling lyrics view as transcript comes in. */}
      <LyricsDisplay artist="olivia-rodrigo" title="traitor" transcript={transcript} />

      {/* Camera -> MediaPipe -> your trained classifier -> chord name */}
      <GestureDetector onGesture={setCurrentGesture} />

      {/* Plays the piano sample for whatever chord the gesture maps to */}
      <ChordSynth gesture={currentGesture} />

      {/* Mic -> backend WebSocket -> OpenAI Realtime API -> live text */}
      <AudioTranscriber onTranscript={setTranscript} />
    </main>
  );
}

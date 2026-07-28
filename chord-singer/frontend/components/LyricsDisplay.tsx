"use client";

import { useEffect, useState } from "react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

type Section = { lyric_line: string; chords: string[] };

export default function LyricsDisplay({
  artist,
  title,
  transcript,
}: {
  artist: string;
  title: string;
  transcript: string;
}) {
  const [sections, setSections] = useState<Section[]>([]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/songs/${artist}/${title}`)
      .then((r) => r.json())
      .then((data) => setSections(data.sections ?? []));
  }, [artist, title]);

  // TODO: match `transcript` against sections to figure out which line
  // is currently being sung, and highlight it - e.g. fuzzy-match the last
  // few words of the transcript against each lyric_line.

  return (
    <div>
      {sections.map((s, i) => (
        <p key={i}>{s.lyric_line}</p>
      ))}
      <p style={{ opacity: 0.5 }}>Live: {transcript}</p>
    </div>
  );
}

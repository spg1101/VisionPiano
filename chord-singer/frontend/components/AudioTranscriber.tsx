"use client";

import { useEffect, useRef } from "react";

const BACKEND_WS_URL = process.env.NEXT_PUBLIC_BACKEND_WS_URL ?? "ws://localhost:8000/realtime/ws";

export default function AudioTranscriber({ onTranscript }: { onTranscript: (text: string) => void }) {
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let cancelled = false;
    let audioContext: AudioContext;
    let processor: ScriptProcessorNode; // fine for a first pass; swap for
    // an AudioWorkletNode later - ScriptProcessorNode is deprecated but
    // still works everywhere and is simpler to get running first.

    async function setup() {
      const socket = new WebSocket(BACKEND_WS_URL);
      socketRef.current = socket;

      socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === "transcript") onTranscript(msg.text);
      };

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContext = new AudioContext();
      const source = audioContext.createMediaStreamSource(stream);
      processor = audioContext.createScriptProcessor(4096, 1, 1);

      processor.onaudioprocess = (event) => {
        if (cancelled || socket.readyState !== WebSocket.OPEN) return;
        const input = event.inputBuffer.getChannelData(0);
        // TODO: convert Float32 samples to the PCM16 format the backend/
        // Realtime API expects before sending.
        socket.send(input.buffer);
      };

      source.connect(processor);
      processor.connect(audioContext.destination);
    }

    setup();
    return () => {
      cancelled = true;
      socketRef.current?.close();
    };
  }, [onTranscript]);

  return null;
}

"use client";

import { useEffect, useRef } from "react";
import { initHandLandmarker, detectLandmarks } from "../lib/mediapipeHands";
import { loadGestureModel, classifyGesture } from "../lib/gestureClassifier";

export default function GestureDetector({ onGesture }: { onGesture: (g: string | null) => void }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    let cancelled = false;
    let rafId: number;

    async function setup() {
      await initHandLandmarker();
      await loadGestureModel();

      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      function tick() {
        if (cancelled || !videoRef.current) return;
        const landmarks = detectLandmarks(videoRef.current, performance.now());
        if (landmarks) {
          const gesture = classifyGesture(landmarks);
          onGesture(gesture);
        } else {
          onGesture(null);
        }
        rafId = requestAnimationFrame(tick);
      }
      tick();
    }

    setup();
    return () => {
      cancelled = true;
      cancelAnimationFrame(rafId);
    };
  }, [onGesture]);

  return <video ref={videoRef} style={{ display: "none" }} playsInline muted />;
}

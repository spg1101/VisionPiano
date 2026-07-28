import { HandLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";

let handLandmarker: HandLandmarker | null = null;

export async function initHandLandmarker() {
  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
  );
  handLandmarker = await HandLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
    },
    numHands: 1,
    runningMode: "VIDEO",
  });
  return handLandmarker;
}

/**
 * Call this once per animation frame with the current video element.
 * Returns 21 landmarks (x, y, z each 0-1 normalized) or null if no hand
 * is detected in this frame.
 */
export function detectLandmarks(video: HTMLVideoElement, timestampMs: number) {
  if (!handLandmarker) return null;
  const result = handLandmarker.detectForVideo(video, timestampMs);
  if (!result.landmarks || result.landmarks.length === 0) return null;
  return result.landmarks[0]; // array of 21 {x, y, z} points
}

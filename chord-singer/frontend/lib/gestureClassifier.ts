import * as tf from "@tensorflow/tfjs";

// This ordering must exactly match the label order used when training in
// ml-training/train.py, and the class names it was exported with.
export const GESTURE_LABELS = ["1_finger", "2_fingers", "3_fingers", "4_fingers", "5_fingers"];

type Landmark = { x: number; y: number; z: number };

/**
 * Mirrors ml-training/normalize.py exactly - if you change the normalization
 * logic during training, update it here too, or the live model will see
 * differently-shaped inputs than it was trained on.
 */
export function normalizeLandmarks(landmarks: Landmark[]): number[] {
  const wrist = landmarks[0];
  const middleTip = landmarks[12];
  const scale = Math.hypot(middleTip.x - wrist.x, middleTip.y - wrist.y, middleTip.z - wrist.z) || 1;

  const features: number[] = [];
  for (const point of landmarks) {
    features.push((point.x - wrist.x) / scale);
    features.push((point.y - wrist.y) / scale);
    features.push((point.z - wrist.z) / scale);
  }
  return features; // length 63 (21 points * 3 coords)
}

let model: tf.LayersModel | null = null;

export async function loadGestureModel() {
  model = await tf.loadLayersModel("/models/gesture-classifier/model.json");
  return model;
}

export function classifyGesture(landmarks: Landmark[]): string | null {
  if (!model) return null;
  const features = normalizeLandmarks(landmarks);
  const prediction = tf.tidy(() => {
    const input = tf.tensor2d([features]);
    const output = model!.predict(input) as tf.Tensor;
    return output.argMax(-1).dataSync()[0];
  });
  return GESTURE_LABELS[prediction] ?? null;
}

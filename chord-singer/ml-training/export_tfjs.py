"""
Converts the trained .h5 model to TensorFlow.js format and drops it directly
into the frontend project so it's ready to load client-side.

Usage: python export_tfjs.py
"""
from pathlib import Path

import tensorflowjs as tfjs
import tensorflow as tf

MODELS_DIR = Path(__file__).parent / "models"
FRONTEND_OUTPUT_DIR = Path(__file__).parent.parent / "frontend" / "public" / "models" / "gesture-classifier"


def main():
    model = tf.keras.models.load_model(MODELS_DIR / "gesture_classifier.h5")
    FRONTEND_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tfjs.converters.save_keras_model(model, str(FRONTEND_OUTPUT_DIR))
    print(f"Exported TFJS model to {FRONTEND_OUTPUT_DIR}")
    print("frontend/lib/gestureClassifier.ts loads it from /models/gesture-classifier/model.json")


if __name__ == "__main__":
    main()

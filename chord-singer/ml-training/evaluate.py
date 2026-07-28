"""
Loads the trained model and prints a confusion matrix so you can see which
gestures get mixed up - that tells you where to record more/better data.

Usage: python evaluate.py
"""
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from normalize import normalize_batch
from train import load_dataset

MODELS_DIR = Path(__file__).parent / "models"

with open(Path(__file__).parent / "labels.json") as f:
    LABELS = json.load(f)
LABEL_NAMES = [name for name, _ in sorted(LABELS.items(), key=lambda kv: kv[1])]


def main():
    model = tf.keras.models.load_model(MODELS_DIR / "gesture_classifier.h5")

    X_raw, y = load_dataset()
    X = normalize_batch(X_raw)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    y_pred = np.argmax(model.predict(X_test), axis=1)

    print(classification_report(y_test, y_pred, target_names=LABEL_NAMES))
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()

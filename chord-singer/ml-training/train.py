"""
Trains a small classifier on the recorded, labeled landmark data.

Run after record_landmarks.py has produced data/<label>.csv for every
gesture in labels.json.

Usage: python train.py
Outputs: models/gesture_classifier.h5, plus prints held-out accuracy.
"""
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from normalize import normalize_batch

DATA_DIR = Path(__file__).parent / "data"
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

with open(Path(__file__).parent / "labels.json") as f:
    LABELS = json.load(f)  # {"1_finger": 0, "2_fingers": 1, ...}


def load_dataset():
    X, y = [], []
    for label_name, label_idx in LABELS.items():
        csv_path = DATA_DIR / f"{label_name}.csv"
        if not csv_path.exists():
            print(f"Warning: no data for '{label_name}' - skipping")
            continue
        rows = np.loadtxt(csv_path, delimiter=",")
        rows = rows.reshape(-1, 63)  # in case there's only one row
        X.append(rows)
        y.extend([label_idx] * len(rows))
    return np.vstack(X), np.array(y)


def build_model(num_classes: int) -> tf.keras.Model:
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(63,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def main():
    X_raw, y = load_dataset()
    X = normalize_batch(X_raw)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = build_model(num_classes=len(LABELS))
    model.fit(X_train, y_train, epochs=50, validation_split=0.1, verbose=1)

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nHeld-out test accuracy: {accuracy:.3f}")

    model.save(MODELS_DIR / "gesture_classifier.h5")
    print(f"Saved model to {MODELS_DIR / 'gesture_classifier.h5'}")


if __name__ == "__main__":
    main()

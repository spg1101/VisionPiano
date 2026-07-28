"""
Normalizes raw (x, y, z) landmark rows to be position- and scale-invariant.

IMPORTANT: this logic must match frontend/lib/gestureClassifier.ts exactly -
the model is trained on features shaped this way, so the live app has to
compute features the same way at inference time.
"""
import numpy as np

WRIST_IDX = 0
MIDDLE_TIP_IDX = 12


def normalize_row(row: np.ndarray) -> np.ndarray:
    """row: flat array of 63 floats (21 landmarks * xyz) -> normalized 63 floats."""
    points = row.reshape(21, 3)
    wrist = points[WRIST_IDX]
    middle_tip = points[MIDDLE_TIP_IDX]
    scale = np.linalg.norm(middle_tip - wrist) or 1.0

    normalized = (points - wrist) / scale
    return normalized.flatten()


def normalize_batch(rows: np.ndarray) -> np.ndarray:
    return np.array([normalize_row(r) for r in rows])

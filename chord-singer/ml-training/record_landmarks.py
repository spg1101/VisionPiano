"""
Records labeled hand landmark samples from your webcam.

Usage:
    python record_landmarks.py 1_finger
    python record_landmarks.py 2_fingers
    ...

Hold the gesture steady in front of the camera. Press SPACE to capture a
frame, 'q' to quit. Aim for 50-100 captures per gesture, varying your hand's
angle and distance from the camera a bit each time.

Appends rows to data/<label>.csv, each row = 63 floats (21 landmarks * xyz).
"""
import csv
import sys
from pathlib import Path

import cv2
import mediapipe as mp

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def main(label: str):
    out_path = DATA_DIR / f"{label}.csv"
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    captured = 0

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands, \
            open(out_path, "a", newline="") as f:
        writer = csv.writer(f)

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.putText(frame, f"label={label}  captured={captured}  [SPACE]=capture [q]=quit",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow("record_landmarks", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord(" ") and result.multi_hand_landmarks:
                row = []
                for point in result.multi_hand_landmarks[0].landmark:
                    row.extend([point.x, point.y, point.z])
                writer.writerow(row)
                captured += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved {captured} samples to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python record_landmarks.py <label>")
        sys.exit(1)
    main(sys.argv[1])

import sys
import os
sys.path.append(os.getcwd())
import cv2
import numpy as np
from pathlib import Path
from training.calibrate_serial_detector import detect_alphabet_in_serial

# Test across 30 genuine notes from dataset
false_positives = 0
total_tested = 0

for p in list(Path("dataset/test/genuine").glob("*.jpg")) + list(Path("dataset/train/genuine").glob("*.jpg"))[:30]:
    img = cv2.imread(str(p))
    if img is None:
        continue
    flag, ed, info = detect_alphabet_in_serial(img)
    total_tested += 1
    if flag:
        # Check if the note actually had something
        false_positives += 1
        print(f"FP: {p.name} | {info}")

print(f"\nTested {total_tested} genuine notes: {false_positives} false positives ({false_positives/total_tested*100:.1f}%)")

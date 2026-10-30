import cv2
import numpy as np
from pathlib import Path

def detect_alphabet_in_serial(img_bgr):
    """
    Detects whether an extraneous alphabet character / inset letter is present
    in between the prefix and the 6-digit serial number sequence.
    """
    h, w = img_bgr.shape[:2]
    if h == 0 or w == 0:
        return False, 0.0, "Empty image"

    # Evaluate Mahatma Gandhi series bottom-left serial number region
    y0, y1 = int(h * 0.60), int(h * 0.85)
    x0, x1 = int(w * 0.17), int(w * 0.45)
    roi = img_bgr[y0:y1, x0:x1]
    if roi.shape[0] < 20 or roi.shape[1] < 50:
        return False, 0.0, "ROI too small"

    roi_h, roi_w = roi.shape[:2]

    # Gap region between prefix (e.g. 2MA) and numeric digits (e.g. 384765)
    # The prefix spans x: 0% to ~28%
    # The middle gap is at x: 28% to 48%
    # The digits span x: 48% to 100%
    gap_x0 = int(roi_w * 0.28)
    gap_x1 = int(roi_w * 0.48)
    gap_roi = roi[:, gap_x0:gap_x1]

    gray_gap = cv2.cvtColor(gap_roi, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge analysis
    edges = cv2.Canny(gray_gap, 35, 100)
    edge_density = float(np.sum(edges > 0)) / (gap_roi.shape[0] * gap_roi.shape[1])
    
    # 2. Contour analysis for letter shapes
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    has_letter_contour = False
    for c in contours:
        cx, cy, cw, ch = cv2.boundingRect(c)
        # Letter height must be significant relative to ROI height (at least 28%)
        # and width between 10% and 80% of gap width
        if ch >= roi_h * 0.28 and cw >= gap_roi.shape[1] * 0.15:
            has_letter_contour = True
            break

    # 3. Text contrast / Sobel variance
    sobel_x = cv2.Sobel(gray_gap, cv2.CV_64F, 1, 0, ksize=3)
    sobel_var = float(np.var(sobel_x))

    # In authentic clean serial numbers, gap is empty background with low edge density and no letter contours.
    # When an alphabet character is placed in between the serial number, both edge density and letter contour are present.
    detected = (has_letter_contour and edge_density > 0.055) or (edge_density > 0.09 and sobel_var > 1200)

    return detected, edge_density, f"has_letter_contour={has_letter_contour}, edge_density={edge_density:.4f}, sobel_var={sobel_var:.1f}"

# Test 1: User Uploaded Note
user_img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
flag, ed, info = detect_alphabet_in_serial(user_img)
print(f"User Uploaded Note (Fake with Alphabet): Detected = {flag} | {info}")

# Test 2: Generated Alphabet Samples
print("\nGenerated Fake Alphabet Samples (First 5):")
for p in list(Path("dataset/train/fake").glob("note_fake_alphabet_in_serial_*.jpg"))[:5]:
    img = cv2.imread(str(p))
    flag, ed, info = detect_alphabet_in_serial(img)
    print(f"  {p.name}: Detected = {flag} | {info}")

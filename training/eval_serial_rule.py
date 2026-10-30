import cv2
import numpy as np
from pathlib import Path

def evaluate_serial_in_between_letter(img_bgr):
    """
    Evaluates whether an extraneous alphabet/character is present
    in between the serial number prefix and the 6-digit sequence.
    """
    h, w = img_bgr.shape[:2]
    # Serial number panel is located in bottom-left zone:
    # y: 60% to 85%, x: 18% to 45%
    x0, x1 = int(w * 0.17), int(w * 0.45)
    y0, y1 = int(h * 0.60), int(h * 0.85)
    roi = img_bgr[y0:y1, x0:x1]
    if roi.size == 0:
        return False, 0.0, "Invalid ROI"
        
    roi_h, roi_w = roi.shape[:2]
    # In standard notes:
    # Left: 3 prefix characters (x: 0 to ~30%)
    # Gap: space between prefix and digits (x: ~30% to ~45%)
    # Right: 6 serial digits (x: ~45% to 100%)
    gap_x0 = int(roi_w * 0.28)
    gap_x1 = int(roi_w * 0.48)
    gap_roi = roi[:, gap_x0:gap_x1]
    
    gray_gap = cv2.cvtColor(gap_roi, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge detection in the gap area
    edges = cv2.Canny(gray_gap, 30, 90)
    edge_density = float(np.sum(edges > 0)) / (gap_roi.shape[0] * gap_roi.shape[1])
    
    # 2. In genuine notes without an alphabet in between, this gap is empty/uniform.
    # When a distinct alphabet letter is printed in between the serial number,
    # it exhibits strong localized contours and vertical strokes.
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    has_large_letter_contour = False
    for c in contours:
        cx, cy, cw, ch = cv2.boundingRect(c)
        if ch > roi_h * 0.35 and cw > roi_w * 0.04:  # Substantial height letter
            has_large_letter_contour = True
            break
            
    # Also check Sobel variance
    sobel_v = float(np.var(cv2.Sobel(gray_gap, cv2.CV_64F, 1, 0, ksize=3)))
    
    has_alphabet = (edge_density > 0.045 and has_large_letter_contour) or (edge_density > 0.08)
    return has_alphabet, edge_density, f"edge_density={edge_density:.4f}, contour={has_large_letter_contour}, sobel_var={sobel_v:.1f}"

# Test on the uploaded image
user_img = cv2.imread("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
flag, ed, info = evaluate_serial_in_between_letter(user_img)
print(f"User Uploaded Note: has_alphabet_in_serial = {flag} | {info}")

# Test on 10 genuine notes from dataset/test
print("\nTesting on genuine notes:")
for p in list(Path("dataset/test/genuine").glob("*.jpg"))[:10]:
    g_img = cv2.imread(str(p))
    if g_img is not None:
        g_flag, g_ed, g_info = evaluate_serial_in_between_letter(g_img)
        print(f"{p.name[:25]:25} | has_alphabet = {g_flag:5} | {g_info}")

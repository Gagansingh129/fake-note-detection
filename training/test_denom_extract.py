import cv2
import numpy as np
from pathlib import Path

def extract_denomination_numeral(img_bgr):
    """
    Extracts the printed numeric denomination from the right-center
    banknote numeral zone (e.g. 10, 20, 50, 100, 200, 500, 1000, 2000).
    """
    h, w = img_bgr.shape[:2]
    # Right-center numeral region:
    # y: 50% to 85%, x: 65% to 88%
    x0, x1 = int(w * 0.65), int(w * 0.88)
    y0, y1 = int(h * 0.50), int(h * 0.85)
    roi = img_bgr[y0:y1, x0:x1]
    if roi.size == 0:
        return None

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Binarize
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Filter text-like components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    roi_h, roi_w = roi.shape[:2]
    
    char_boxes = []
    for i in range(1, num_labels):
        x, y, cw, ch, area = stats[i]
        # Digit proportions on Indian banknotes:
        # Height is typically 30% to 80% of the numeral ROI
        # Aspect ratio (w/h) is typically 0.2 to 0.95
        if roi_h * 0.25 <= ch <= roi_h * 0.90 and 0.15 <= cw / ch <= 1.2 and area > 100:
            char_boxes.append((x, y, cw, ch, area, centroids[i]))
            
    # Sort left to right
    char_boxes.sort(key=lambda b: b[0])
    
    # Find aligned group with similar height and y-position
    if not char_boxes:
        return None
        
    return len(char_boxes), [(b[0], b[1], b[2], b[3]) for b in char_boxes]

# Test on the user camera bogus note
user_img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
res = extract_denomination_numeral(user_img)
print("User Bogus Note Numeral Zone:", res)

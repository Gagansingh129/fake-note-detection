import cv2
import numpy as np

roi = cv2.imread("backend/uploads/crop_denom_1000.jpg")
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Otsu thresholding or adaptive thresholding
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imwrite("backend/uploads/crop_denom_thresh.png", thresh)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Found {len(contours)} contours:")
boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if h > 15 and w > 8:
        boxes.append((x, y, w, h, cv2.contourArea(c)))

boxes.sort(key=lambda b: b[0])
for idx, b in enumerate(boxes):
    print(f"  Contour {idx}: x={b[0]}, y={b[1]}, w={b[2]}, h={b[3]}, area={b[4]}")

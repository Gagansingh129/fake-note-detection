import cv2
import numpy as np

roi = cv2.imread("backend/uploads/serial_roi.png")
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
text_mask = (gray < 110).astype(np.uint8) * 255
cv2.imwrite("backend/uploads/text_mask.png", text_mask)

# Find connected components in text_mask
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(text_mask)
print(f"Detected {num_labels - 1} text components:")
boxes = []
for i in range(1, num_labels):
    x, y, w, h, area = stats[i]
    if area > 10 and h > 8:
        boxes.append((x, y, w, h, area))

boxes.sort(key=lambda b: b[0])
for idx, b in enumerate(boxes):
    print(f"Char {idx}: x={b[0]}, y={b[1]}, w={b[2]}, h={b[3]}, area={b[4]}")

import cv2
import numpy as np

tr_img = cv2.imread("backend/uploads/slice_tr.jpg")
gray_tr = cv2.cvtColor(tr_img, cv2.COLOR_BGR2GRAY)
_, thresh_tr = cv2.threshold(gray_tr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh_tr)
print(f"Top Right components ({num_labels}):")
boxes = []
for i in range(1, num_labels):
    x, y, w, h, a = stats[i]
    if h > 20 and w > 10 and a > 100:
        boxes.append((x, y, w, h, a))
boxes.sort(key=lambda b: b[0])
for b in boxes:
    print(f"  x={b[0]}, y={b[1]}, w={b[2]}, h={b[3]}, area={b[4]}")

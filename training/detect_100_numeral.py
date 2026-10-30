import cv2
import numpy as np

# In Indian 100 notes (both Mahatma Gandhi Old and New Series):
# Let's check for the digits "100"
# In Old series 100 note:
# Center has: a large "100" right above "एक सौ रुपये"
# Top right has: "100"
# Bottom left has: serial number
# Bottom right has: "100" watermark window or Gandhi

# Let's inspect slice_center.jpg:
c_img = cv2.imread("backend/uploads/slice_center.jpg")
gray_c = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
_, thresh_c = cv2.threshold(gray_c, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imwrite("backend/uploads/slice_center_thresh.png", thresh_c)

# Let's inspect slice_tr.jpg:
tr_img = cv2.imread("backend/uploads/slice_tr.jpg")
gray_tr = cv2.cvtColor(tr_img, cv2.COLOR_BGR2GRAY)
_, thresh_tr = cv2.threshold(gray_tr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imwrite("backend/uploads/slice_tr_thresh.png", thresh_tr)

# Check connected components in center for "100"
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh_c)
print(f"Center components ({num_labels}):")
boxes = []
for i in range(1, num_labels):
    x, y, w, h, a = stats[i]
    if h > 20 and w > 10 and a > 100:
        boxes.append((x, y, w, h, a))
boxes.sort(key=lambda b: b[0])
for b in boxes:
    print(f"  x={b[0]}, y={b[1]}, w={b[2]}, h={b[3]}, area={b[4]}")

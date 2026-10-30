import cv2
import numpy as np

img = cv2.imread("backend/uploads/upload_1793237397580_camera_845bd47ad1dd4c9f91b8d0f4bacfb012.jpg")
h, w = img.shape[:2]

# Let's save 6 slices to inspect:
# 1. Top left (0.0 to 0.4 w, 0.0 to 0.4 h)
cv2.imwrite("backend/uploads/slice_tl.jpg", img[:int(h*0.45), :int(w*0.4)])
# 2. Top right (0.6 to 1.0 w, 0.0 to 0.45 h)
cv2.imwrite("backend/uploads/slice_tr.jpg", img[:int(h*0.45), int(w*0.6):])
# 3. Center (0.35 to 0.65 w, 0.1 to 0.9 h)
cv2.imwrite("backend/uploads/slice_center.jpg", img[:, int(w*0.35):int(w*0.65)])
# 4. Bottom left (0.0 to 0.4 w, 0.55 to 1.0 h)
cv2.imwrite("backend/uploads/slice_bl.jpg", img[int(h*0.55):, :int(w*0.4)])
# 5. Bottom right (0.6 to 1.0 w, 0.55 to 1.0 h)
cv2.imwrite("backend/uploads/slice_br.jpg", img[int(h*0.55):, int(w*0.6):])

print("Saved all 5 slices.")

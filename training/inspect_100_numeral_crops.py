import cv2
import numpy as np

img = cv2.imread("backend/uploads/user_camera_note_100.jpg")
h, w = img.shape[:2]

# Let's inspect where "100" is on this note:
# Center zone: y: 15% to 55%, x: 35% to 65%
# Top right zone: y: 5% to 35%, x: 75% to 95%
center_roi = img[int(h*0.15):int(h*0.55), int(w*0.35):int(w*0.65)]
cv2.imwrite("backend/uploads/crop_100_center.jpg", center_roi)

tr_roi = img[int(h*0.05):int(h*0.35), int(w*0.75):int(w*0.95)]
cv2.imwrite("backend/uploads/crop_100_tr.jpg", tr_roi)

print("Saved crop_100_center.jpg and crop_100_tr.jpg")

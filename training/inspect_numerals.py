import cv2
import numpy as np

img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
h, w = img.shape[:2]
print("Image size:", w, h)

# Let's crop the right-center denomination zone where "1000" is located:
# In the image, "1000" is at roughly x: 65% to 85%, y: 55% to 85%
x0, x1 = int(w * 0.65), int(w * 0.88)
y0, y1 = int(h * 0.52), int(h * 0.88)
roi_denom = img[y0:y1, x0:x1]
cv2.imwrite("backend/uploads/crop_denom_1000.jpg", roi_denom)
print("Saved crop_denom_1000.jpg")

# Also crop the left vertical strip where "2000" is located:
# x: 5% to 20%, y: 15% to 75%
lx0, lx1 = int(w * 0.05), int(w * 0.22)
ly0, ly1 = int(h * 0.15), int(h * 0.80)
roi_left = img[ly0:ly1, lx0:lx1]
cv2.imwrite("backend/uploads/crop_denom_left.jpg", roi_left)
print("Saved crop_denom_left.jpg")

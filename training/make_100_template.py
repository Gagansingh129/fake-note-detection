import cv2
import numpy as np

c_img = cv2.imread("backend/uploads/crop_100_center.jpg")
gray = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imwrite("backend/uploads/crop_100_center_thresh.png", thresh)

# Let's save a template of "100" from this center crop
# The large "100" numeral
ch, cw = c_img.shape[:2]
# Numeral 100 in center
template_100 = c_img[int(ch*0.15):int(ch*0.75), int(cw*0.20):int(cw*0.80)]
cv2.imwrite("backend/models/template_100.png", template_100)
print("Saved template_100.png with shape:", template_100.shape)

# Test template matching on the full note
img = cv2.imread("backend/uploads/user_camera_note_100.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_tpl = cv2.cvtColor(template_100, cv2.COLOR_BGR2GRAY)

res = cv2.matchTemplate(gray_img, gray_tpl, cv2.TM_CCOEFF_NORMED)
_, max_v, _, max_loc = cv2.minMaxLoc(res)
print(f"Match correlation on user 100 note: {max_v:.4f} at {max_loc}")

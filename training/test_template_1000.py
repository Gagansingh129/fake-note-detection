import cv2
import numpy as np

roi = cv2.imread("backend/uploads/crop_denom_1000.jpg")
h, w = roi.shape[:2]
# The ₹1000 numeral:
denom_1000_patch = roi[15:75, 15:170]
cv2.imwrite("backend/uploads/template_1000.png", denom_1000_patch)
print("Saved template_1000.png with shape:", denom_1000_patch.shape)

# Test template matching on the whole image
img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_tpl = cv2.cvtColor(denom_1000_patch, cv2.COLOR_BGR2GRAY)

res = cv2.matchTemplate(gray_img, gray_tpl, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(f"Match correlation on bogus note: {max_val:.4f} at {max_loc}")

# Test template matching on real 2000 note
real_2000 = cv2.imread("dataset/raw/genuine/note_2000_Rs_2000_0129.jpg")
gray_real = cv2.cvtColor(real_2000, cv2.COLOR_BGR2GRAY)
res_real = cv2.matchTemplate(gray_real, gray_tpl, cv2.TM_CCOEFF_NORMED)
_, max_val_real, _, _ = cv2.minMaxLoc(res_real)
print(f"Match correlation on real 2000 note: {max_val_real:.4f}")

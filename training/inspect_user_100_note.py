import cv2
import numpy as np

img = cv2.imread("backend/uploads/user_camera_note_100.jpg")
h, w = img.shape[:2]

# Let's crop several regions of the note:
# Center
center_crop = img[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
cv2.imwrite("backend/uploads/debug_100_center.jpg", center_crop)

# Let's crop the bottom left (where 100 or serial or emblem is)
bl_crop = img[int(h*0.5):int(h*0.9), int(w*0.1):int(w*0.4)]
cv2.imwrite("backend/uploads/debug_100_bl.jpg", bl_crop)

# Top right
tr_crop = img[int(h*0.1):int(h*0.5), int(w*0.6):int(w*0.9)]
cv2.imwrite("backend/uploads/debug_100_tr.jpg", tr_crop)

# Let's check mean BGR of this note
print("Mean BGR of note:", np.mean(img, axis=(0,1)))

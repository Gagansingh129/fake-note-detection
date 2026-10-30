import cv2
import numpy as np

img = cv2.imread("backend/uploads/user_camera_note_100.jpg")
h, w = img.shape[:2]

# Search for "100" numeral on the note
# In Indian 100 notes:
# Old series has "100" at top right and center:
# New series has "100" at center right and bottom right
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Let's save a grayscale version
cv2.imwrite("backend/uploads/debug_100_gray.jpg", gray)

# Let's inspect where numerals are
print("Image dimensions:", w, h)

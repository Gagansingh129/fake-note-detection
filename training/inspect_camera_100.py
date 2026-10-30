import cv2
import numpy as np

img_path = "backend/uploads/upload_1793237397580_camera_845bd47ad1dd4c9f91b8d0f4bacfb012.jpg"
img = cv2.imread(img_path)
print("Shape:", img.shape if img is not None else None)

if img is not None:
    cv2.imwrite("backend/uploads/user_camera_note_100.jpg", img)
    print("Saved user_camera_note_100.jpg")

import cv2
import numpy as np

img_path = "backend/uploads/upload_1793208914788_camera_2ab1c60c7c41468b99e20610e64cde12.jpg"
img = cv2.imread(img_path)
print("Image shape:", img.shape if img is not None else "None")

# Copy to a clearly named debug image so we can inspect
if img is not None:
    cv2.imwrite("backend/uploads/user_camera_bogus_note.jpg", img)
    print("Saved to backend/uploads/user_camera_bogus_note.jpg")

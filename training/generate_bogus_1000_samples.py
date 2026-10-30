import sys
sys.stdout.reconfigure(encoding='utf-8')
import cv2
import numpy as np
import random
from pathlib import Path

# Load user camera bogus note
src_path = Path("backend/uploads/user_camera_bogus_note.jpg")
base_img = cv2.imread(str(src_path))
if base_img is None:
    raise RuntimeError(f"Could not load image from {src_path}")

h, w = base_img.shape[:2]
TOTAL_SAMPLES = 120

dirs = [
    Path("dataset/raw/fake"),
    Path("dataset/train/fake"),
    Path("dataset/validation/fake"),
]
for d in dirs:
    d.mkdir(parents=True, exist_ok=True)

for i in range(TOTAL_SAMPLES):
    img = base_img.copy()

    # 1. Random Brightness & Contrast
    alpha = random.uniform(0.75, 1.25)
    beta = random.uniform(-25, 25)
    img = np.clip(alpha * img.astype(np.float32) + beta, 0, 255).astype(np.uint8)

    # 2. Random Rotation (-5 to 5 deg)
    angle = random.uniform(-5.0, 5.0)
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 3. Random Slight Crop & Zoom
    crop_pct = random.uniform(0.01, 0.08)
    dx = int(w * crop_pct)
    dy = int(h * crop_pct)
    cropped = img[dy:h-dy, dx:w-dx]
    img = cv2.resize(cropped, (w, h))

    # 4. Blur / Sharpness
    if random.random() < 0.35:
        k = random.choice([3, 5])
        img = cv2.GaussianBlur(img, (k, k), 0)
    elif random.random() < 0.35:
        kernel = np.array([[0, -0.5, 0], [-0.5, 3.0, -0.5], [0, -0.5, 0]])
        img = np.clip(cv2.filter2D(img, -1, kernel), 0, 255).astype(np.uint8)

    # 5. Gaussian Noise
    if random.random() < 0.3:
        noise = np.random.normal(0, random.uniform(3, 10), img.shape)
        img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    filename = f"note_fake_bogus_1000_{i+1:03d}.jpg"
    cv2.imwrite(str(Path("dataset/raw/fake") / filename), img)

    # 80% train, 20% validation
    if i < int(TOTAL_SAMPLES * 0.8):
        cv2.imwrite(str(Path("dataset/train/fake") / filename), img)
    else:
        cv2.imwrite(str(Path("dataset/validation/fake") / filename), img)

print(f"Successfully generated {TOTAL_SAMPLES} augmented training & validation samples of bogus ₹1000 note.")

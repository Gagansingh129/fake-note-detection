import cv2
import numpy as np
import random
from pathlib import Path

# Source user uploaded note
src_path = Path("C:/Users/LOQ/.gemini/antigravity/brain/0f373fd0-4e75-4641-95b1-827638427e84/.user_uploaded/media_1793200655833_2c1f6c8c.png")
base_img = cv2.imread(str(src_path))
if base_img is None:
    raise RuntimeError(f"Could not load source image from {src_path}")

print(f"Loaded base fake note with alphabet in serial: {base_img.shape}")

# Target directories
dirs = [
    Path("dataset/raw/fake"),
    Path("dataset/train/fake"),
    Path("dataset/train/100/fake"),
    Path("dataset/validation/fake"),
    Path("dataset/validation/100/fake"),
]
for d in dirs:
    d.mkdir(parents=True, exist_ok=True)

# Generate diverse augmentations
TOTAL_SAMPLES = 120
letters = ["B", "A", "C", "D", "E", "F", "K", "M", "R", "S", "X"]

h, w = base_img.shape[:2]

for i in range(TOTAL_SAMPLES):
    img = base_img.copy()

    # 1. Random Brightness and Contrast
    alpha = random.uniform(0.75, 1.25) # contrast
    beta = random.uniform(-25, 25)     # brightness
    img = np.clip(alpha * img.astype(np.float32) + beta, 0, 255).astype(np.uint8)

    # 2. Random Slight Rotation / Perspective
    angle = random.uniform(-4.0, 4.0)
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 3. Random Slight Crop / Zoom (simulate different camera distances)
    crop_pct = random.uniform(0.01, 0.08)
    dx = int(w * crop_pct)
    dy = int(h * crop_pct)
    cropped = img[dy:h-dy, dx:w-dx]
    img = cv2.resize(cropped, (w, h))

    # 4. Optional subtle blur or sharpness
    if random.random() < 0.35:
        ksize = random.choice([3, 5])
        img = cv2.GaussianBlur(img, (ksize, ksize), 0)
    elif random.random() < 0.35:
        # Subtle sharpening
        kernel = np.array([[0, -0.5, 0], [-0.5, 3.0, -0.5], [0, -0.5, 0]])
        img = np.clip(cv2.filter2D(img, -1, kernel), 0, 255).astype(np.uint8)

    # 5. Gaussian Sensor Noise
    if random.random() < 0.3:
        noise = np.random.normal(0, random.uniform(3, 10), img.shape)
        img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    # 6. For some samples, vary the alphabet letter in the serial number
    if random.random() < 0.5:
        letter_choice = random.choice(letters)
        # Position of the letter in between 2MA and 384765
        lx0, lx1 = int(w * 0.28), int(w * 0.35)
        ly0, ly1 = int(h * 0.65), int(h * 0.79)
        # Add slight variation or text stamp of another alphabet
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = random.uniform(0.7, 0.9)
        color = (random.randint(20, 60), random.randint(20, 60), random.randint(20, 60))
        cv2.putText(img, letter_choice, (lx0 + random.randint(-5, 5), ly1 - 5), font, font_scale, color, 2, cv2.LINE_AA)

    filename = f"note_fake_alphabet_in_serial_{i+1:03d}.jpg"

    # Save to raw
    cv2.imwrite(str(Path("dataset/raw/fake") / filename), img)

    # Split: 80% train, 20% validation
    if i < int(TOTAL_SAMPLES * 0.8):
        cv2.imwrite(str(Path("dataset/train/fake") / filename), img)
        cv2.imwrite(str(Path("dataset/train/100/fake") / filename), img)
    else:
        cv2.imwrite(str(Path("dataset/validation/fake") / filename), img)
        cv2.imwrite(str(Path("dataset/validation/100/fake") / filename), img)

print(f"Successfully generated {TOTAL_SAMPLES} augmented training & validation samples of fake note with alphabet in serial number.")

"""
NoteGuard AI - Dummy Note / Toy Currency Augmentation Suite
===========================================================
Adds realistic dummy/novelty banknote specimens (such as "Children Bank of India",
"Manoranjan Bank of India", "Full of Fun", "Coupon Label" notes) into the raw dataset
to train the model to accurately detect and reject toy/dummy currency.
"""

from pathlib import Path
import random
import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOADS_DIR = PROJECT_ROOT / "backend" / "uploads"
RAW_FAKE_DIR = PROJECT_ROOT / "dataset" / "raw" / "fake"
RAW_GENUINE_DIR = PROJECT_ROOT / "dataset" / "raw" / "genuine"

RAW_FAKE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Collect all real user captures of the dummy note from backend/uploads
dummy_capture_files = [
    "upload_1792659078201_camera_d9a332daa52f4948af8879dc43b6187d.jpg",
    "upload_1792659026840_camera_42f8e0dc93fc43c1a142c8f7ec162122.jpg",
    "upload_1792658886491_camera_5243b7f69d4f4331a89e4fd86a7c7c15.jpg",
    "upload_1792658858518_camera_77bcd22d8e684c7ab3030005e906b1e5.jpg",
    "upload_1792658661138_camera_66084ad0601a41e0870df84cbdf0a323.jpg",
    "upload_1792658580067_camera_7139222766414449be548e7099b2a2e1.jpg",
    "upload_1792658544854_camera_a5266d8c1710468692b44829f3c53093.jpg",
    "upload_1792658490588_camera_7831f7871fc44db8a8b8c91f0964333a.jpg"
]

print("=" * 65)
print("   NoteGuard AI - Generating Dummy/Toy Note Training Samples")
print("=" * 65)

generated_count = 0

# A. Process user's physical dummy note captures with diverse camera conditions
for idx, fname in enumerate(dummy_capture_files):
    fpath = UPLOADS_DIR / fname
    if not fpath.exists():
        continue
    
    img = cv2.imread(str(fpath))
    if img is None:
        continue

    # Save original base capture
    base_name = f"note_dummy_fulloffun_camera_{idx+1}_base.jpg"
    cv2.imwrite(str(RAW_FAKE_DIR / base_name), img)
    generated_count += 1

    h, w = img.shape[:2]

    # Generate 12 augmentations per capture
    for aug_i in range(1, 13):
        aug_img = img.copy()

        # 1. Subtle rotation (-6 to +6 degrees)
        angle = random.uniform(-6.0, 6.0)
        M_rot = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        aug_img = cv2.warpAffine(aug_img, M_rot, (w, h), borderMode=cv2.BORDER_REFLECT)

        # 2. Slight zoom (0.93 to 1.07)
        scale = random.uniform(0.93, 1.07)
        new_w, new_h = int(w * scale), int(h * scale)
        scaled = cv2.resize(aug_img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        if scale > 1.0:
            x0 = (new_w - w) // 2
            y0 = (new_h - h) // 2
            aug_img = scaled[y0:y0+h, x0:x0+w]
        else:
            pad_x = (w - new_w) // 2
            pad_y = (h - new_h) // 2
            aug_img = cv2.copyMakeBorder(
                scaled, pad_y, h - new_h - pad_y, pad_x, w - new_w - pad_x,
                cv2.BORDER_REFLECT
            )

        # 3. Brightness & Contrast
        alpha = random.uniform(0.85, 1.20)  # Contrast
        beta = random.uniform(-25.0, 25.0)   # Brightness
        aug_img = cv2.convertScaleAbs(aug_img, alpha=alpha, beta=beta)

        # 4. Color temperature / white balance shift
        b_shift = random.uniform(-10.0, 10.0)
        r_shift = random.uniform(-10.0, 10.0)
        b, g, r = cv2.split(aug_img)
        b = np.clip(b.astype(np.float32) + b_shift, 0, 255).astype(np.uint8)
        r = np.clip(r.astype(np.float32) + r_shift, 0, 255).astype(np.uint8)
        aug_img = cv2.merge([b, g, r])

        # 5. Occasional slight Gaussian focus softening (camera autofocus lag)
        if random.random() < 0.25:
            aug_img = cv2.GaussianBlur(aug_img, (3, 3), 0.7)

        aug_fname = f"note_dummy_fulloffun_camera_{idx+1}_aug_{aug_i:03d}.jpg"
        cv2.imwrite(str(RAW_FAKE_DIR / aug_fname), aug_img)
        generated_count += 1

print(f"[*] Generated {generated_count} camera-adapted dummy note specimens from physical captures.")

# B. Synthesize multi-denomination Dummy / Children Bank notes from genuine note templates
synthetic_count = 0
genuine_templates = list(RAW_GENUINE_DIR.glob("*.jpg"))
random.seed(42)

for i in range(40):
    if not genuine_templates:
        break
    base_template_path = random.choice(genuine_templates)
    base_img = cv2.imread(str(base_template_path))
    if base_img is None:
        continue
    
    bh, bw = base_img.shape[:2]
    toy_note = base_img.copy()

    # 1. Overlay fake solid red/pink security thread strip
    tx0 = int(bw * 0.34)
    tx1 = int(bw * 0.36)
    toy_note[:, tx0:tx1] = (40, 40, 220)  # Bright solid red thread

    # 2. Add "FULL OF FUN" / "CHILDREN BANK" / "MANORANJAN BANK" text
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Watermark box text
    cv2.putText(toy_note, "FULL OF FUN", (int(bw * 0.05), int(bh * 0.25)), font, 0.7, (20, 20, 20), 2, cv2.LINE_AA)
    cv2.putText(toy_note, "CHILDREN BANK", (int(bw * 0.25), int(bh * 0.15)), font, 0.8, (20, 20, 20), 2, cv2.LINE_AA)
    # Right coupon banner
    cv2.rectangle(toy_note, (int(bw * 0.88), 0), (bw, bh), (30, 140, 230), -1)
    cv2.putText(toy_note, "COUPON", (int(bw * 0.89), int(bh * 0.50)), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # 3. Apply color shift (toy notes are often saturated or off-color)
    toy_note = cv2.convertScaleAbs(toy_note, alpha=random.uniform(0.9, 1.15), beta=random.uniform(-10, 15))

    synth_fname = f"note_dummy_synth_childrenbank_{i+1:03d}.jpg"
    cv2.imwrite(str(RAW_FAKE_DIR / synth_fname), toy_note)
    synthetic_count += 1

print(f"[*] Generated {synthetic_count} multi-denomination synthetic dummy currency samples.")
total_dummy = generated_count + synthetic_count
print(f"[*] Total dummy/toy currency specimens added to dataset/raw/fake: {total_dummy}")
print("=" * 65)

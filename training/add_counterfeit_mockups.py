"""
NoteGuard AI - Augment Dataset with Real-World Camera & Mockup Banknotes
=======================================================================
Adds real-world webcam captures of genuine banknotes and camera captures of
novelty / counterfeit app mockups (such as 'Fake Indian Currency Maker' mockups)
into dataset/raw/ to teach deep learning models the exact decision boundary
between physical authentic notes and screen/app mockups.
"""

import os
import shutil
from pathlib import Path
import cv2
import numpy as np

def augment_and_save(src_path: Path, target_dir: Path, prefix: str, count: int = 15):
    img = cv2.imread(str(src_path))
    if img is None:
        print(f"[!] Warning: Could not read {src_path}")
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    saved = 0

    h, w = img.shape[:2]

    # Save original base
    base_name = f"{prefix}_base.jpg"
    cv2.imwrite(str(target_dir / base_name), img)
    saved += 1

    for i in range(count):
        # 1. Mild rotation (-6 to +6 degrees)
        angle = np.random.uniform(-6, 6)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)

        # 2. Brightness variation (0.8 to 1.25)
        alpha = np.random.uniform(0.8, 1.25) # contrast
        beta = np.random.uniform(-20, 25)    # brightness
        adjusted = cv2.convertScaleAbs(rotated, alpha=alpha, beta=beta)

        # 3. Color temperature / channel shift (simulating different phone screens & webcams)
        b, g, r = cv2.split(adjusted)
        b_shift = np.random.uniform(0.9, 1.1)
        r_shift = np.random.uniform(0.9, 1.1)
        b = np.clip(b * b_shift, 0, 255).astype(np.uint8)
        r = np.clip(r * r_shift, 0, 255).astype(np.uint8)
        color_shifted = cv2.merge((b, g, r))

        # 4. Subtle zoom/crop
        zoom = np.random.uniform(0.94, 1.0)
        zh, zw = int(h * zoom), int(w * zoom)
        zy = np.random.randint(0, h - zh + 1)
        zx = np.random.randint(0, w - zw + 1)
        cropped = color_shifted[zy:zy+zh, zx:zx+zw]
        final_img = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_AREA)

        out_name = f"{prefix}_aug_{i+1:03d}.jpg"
        cv2.imwrite(str(target_dir / out_name), final_img)
        saved += 1

    return saved


def run_enrichment():
    raw_genuine = Path("dataset/raw/genuine")
    raw_fake = Path("dataset/raw/fake")

    # 1. Ingest Real 50 Rs Webcam Captures into Genuine
    real_sources = [
        Path("backend/uploads/upload_1792649719885_camera_f1fc952000664deaad7c85a3f4dfeee7.jpg"),
        Path("backend/uploads/upload_1792650597826_camera_1f69ca66e2bb427889f9f7861c8902e4.jpg"),
        Path("scratch/user_note_crop.jpg"),
        Path("scratch/test_detected_roi.jpg")
    ]
    gen_added = 0
    for idx, src in enumerate(real_sources):
        if src.exists():
            c = augment_and_save(src, raw_genuine, f"note_camera_real50_{idx+1}", count=12)
            gen_added += c
            print(f"[*] Ingested {c} augmented genuine samples from {src.name}")

    # 2. Ingest Counterfeit Currency App Mockups into Fake
    fake_sources = [
        Path("backend/uploads/upload_1792651658335_camera_71b17c502f83480583708852df3f049b.jpg"),
        Path("backend/uploads/upload_1792651603785_camera_f452339c60ba4a87be1964ac5ffc6c2b.jpg"),
        Path("backend/uploads/upload_1792651508305_camera_09c9cb18e1204012be9bbbdb185e80e3.jpg")
    ]
    fake_added = 0
    for idx, src in enumerate(fake_sources):
        if src.exists():
            c = augment_and_save(src, raw_fake, f"note_camera_fake_mockup_{idx+1}", count=20)
            fake_added += c
            print(f"[*] Ingested {c} augmented fake mockup samples from {src.name}")

    print("\n" + "=" * 60)
    print("Dataset Camera & Counterfeit Mockup Enrichment Complete!")
    print(f"[*] Added {gen_added} genuine camera-adapted banknote samples.")
    print(f"[*] Added {fake_added} fake mockup / screen-displayed samples.")
    print("=" * 60)

if __name__ == "__main__":
    run_enrichment()

"""
NoteGuard AI - Universal Camera Banknote Ingestion & Augmentation Engine
========================================================================
Extracts and curates real user camera captures across circulating Indian
banknotes (₹5, ₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹2000), creates raw reference sets,
and generates realistic webcam augmentations for both Authenticity and Denomination models.
"""

import os
import sys
import glob
from pathlib import Path
import cv2
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("backend"))
from app.services.image_processing import quality_checker

# Real user camera image mappings
USER_CAMERA_SOURCES = {
    "5": [
        "dataset/denomination/train/5/*.jpg",
        "dataset/denomination/val/5/*.jpg",
    ],
    "10": [
        "scratch/latest_user_uploads/upload_1793594695602_camera_f252234fd3f4471cbdf237bb9c447056.jpg", # ₹10 in hand
        "scratch/latest_user_uploads/upload_1793594721888_camera_6a037e5627894e9890ef2e98d3212533.jpg", # ₹10 old in hand
        "scratch/latest_user_uploads/upload_1793594767336_camera_701a1f8f3082426c9711d93c5b3da314.jpg", # ₹10 on desk 1
        "scratch/latest_user_uploads/upload_1793594801271_camera_eddc91dccd2241bc802dacb0d7675d43.jpg", # ₹10 on desk 2
        "scratch/new_test_scans/*103*.jpg", # ₹10 new
        "scratch/new_test_scans/*106*.jpg", # ₹10 new
        "scratch/new_test_scans/*107*.jpg", # ₹10 new
        "scratch/new_test_scans/*108*.jpg", # ₹10 new
        "scratch/new_test_scans/*109*.jpg", # ₹10 new
        "backend/uploads/*camera*5243b7f6*.jpg",
        "backend/uploads/*camera*42f8e0dc*.jpg",
        "backend/uploads/*camera*d9a332da*.jpg",
        "backend/uploads/*camera*5840dadb*.jpg",
    ],
    "20": [
        "scratch/upload_1793940447693_camera_5ad05b848d1747fd833c01358413029c.jpg", # user real 20 note webcam
        "scratch/upload_1793940522874_camera_16570e0687354465bbd28cfdde138c6d.jpg", # user real 20 note webcam 2
        "backend/uploads/upload_1793933504779_camera_c43ef6201ac94ac29df6ac93928f49ea.jpg", # latest ₹20 held in webcam
        "scratch/actual_banknote_crop.jpg", # cropped ₹20 authentic note
        "scratch/latest_user_uploads/upload_1793594659634_camera_aa72aeba79394d60b86c340dacfde314.jpg", # ₹20 in hand
        "scratch/latest_user_uploads/upload_1793594823730_camera_e020663450f14151a878671b4280d694.jpg", # ₹20 on desk 1
        "scratch/latest_user_uploads/upload_1793594838881_camera_947926ecadd84f66bce0e876b39bf496.jpg", # ₹20 on desk 2
        "scratch/new_test_scans/*104*.jpg", # ₹20 new
        "scratch/new_test_scans/*113*.jpg", # ₹20 new desk
        "backend/uploads/*camera*c43ef620*.jpg",
    ],
    "50": [
        "scratch/repo6/CNN-based-classification-(PRIMARY)/dataset/comp_data/50_*/*.*",
        "dataset/train/genuine/note_camera_real50_*.*",
        "backend/uploads/*camera*23ad5692*.jpg",
        "backend/uploads/*camera*77bcd22d*.jpg",
    ],
    "100": [
        "scratch/upload_1793940479872_camera_7485fe882e3247268dbd139ce49104e7.jpg", # user real 100 note webcam
        "scratch/inspect_user_cam_100_aug_006.jpg", # user real 100 note
        "scratch/latest_user_uploads/upload_1793594635771_camera_7521002a944548d09ab2b463e2ca4bbe.jpg", # ₹100 in hand
        "scratch/latest_user_uploads/upload_1793594863466_camera_839842c48bd54c48b0fa5c9f0cb09f15.jpg", # ₹100 on desk
        "scratch/new_test_scans/*105*.jpg", # ₹100 in hand
        "scratch/new_test_scans/*111*.jpg", # ₹100 on desk
        "scratch/new_test_scans/*112*.jpg", # ₹100 on desk
        "scratch/user_scans/*.jpg",
        "dataset/raw/genuine_100_camera/*.jpg",
        "backend/uploads/*camera*f43a44aa*.jpg",
        "backend/uploads/*camera*3834a544*.jpg",
        "backend/uploads/*camera*baa9fab9*.jpg",
        "backend/uploads/*camera*8b88ef14*.jpg",
        "backend/uploads/*camera*5e662394*.jpg",
        "backend/uploads/*camera*53ba42c3*.jpg",
        "backend/uploads/*camera*264a6202*.jpg",
        "backend/uploads/*camera*2549faaf*.jpg",
    ],
    "200": [
        "scratch/latest_user_uploads/upload_1793594886292_camera_eaeb61ede5e140fbb4acf6926f9b4cb7.jpg", # ₹200 on desk
        "scratch/latest_user_uploads/upload_1793568524991_da3c2db74da44b94b7419d3ca25aa462.1000397013.jpg",
        "scratch/new_test_scans/*110*.jpg", # ₹200 on desk
        "backend/uploads/*camera*deea3ec0*.jpg",
        "backend/uploads/*camera*d1aa3f24*.jpg",
    ],
    "500": [
        "dataset/raw/genuine/*500*.*",
        "scratch/repo6/CNN-based-classification-(PRIMARY)/dataset/comp_data/500_*/*.*",
        "dataset/denomination/train/500/*.jpg",
    ],
    "2000": [
        "dataset/denomination/train/2000/*.jpg",
        "dataset/denomination/val/2000/*.jpg",
        "backend/uploads/*camera*9e5f58ae*.jpg",
        "backend/uploads/*camera*a5266d8c*.jpg",
    ]
}

def augment_camera_note(img_bgr: np.ndarray, index: int) -> np.ndarray:
    """Applies realistic camera variations (perspective, rotation, lighting, white-balance, finger grips)."""
    h, w = img_bgr.shape[:2]
    aug = img_bgr.copy()

    # 1. Perspective / Tilt
    if index % 2 == 1:
        d = int(w * 0.035)
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        dx = ((index % 5) - 2) * (d // 2)
        dy = ((index % 4) - 2) * (d // 2)
        pts2 = np.float32([[dx, dy], [w - dx, dy], [-dx, h - dy], [w + dx, h - dy]])
        M_p = cv2.getPerspectiveTransform(pts1, pts2)
        aug = cv2.warpPerspective(aug, M_p, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 2. Subtle Rotation (-4 to +4 degrees)
    angle = ((index % 5) - 2) * 1.8
    if angle != 0:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        aug = cv2.warpAffine(aug, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 3. Room Lighting Gradients
    if index % 3 == 0:
        grad_dir = index % 4
        if grad_dir == 0:
            grad = np.tile(np.linspace(0.85, 1.15, w), (h, 1))
        elif grad_dir == 1:
            grad = np.tile(np.linspace(1.15, 0.85, w), (h, 1))
        elif grad_dir == 2:
            grad = np.tile(np.linspace(0.88, 1.12, h), (w, 1)).T
        else:
            grad = np.tile(np.linspace(1.12, 0.88, h), (w, 1)).T
        aug = np.clip(aug.astype(np.float32) * grad[:, :, np.newaxis], 0, 255).astype(np.uint8)

    # 4. White Balance / Warmth shifts (simulating warm ceiling bulb vs daylight)
    wb_mode = index % 6
    b, g, r = cv2.split(aug)
    if wb_mode == 1:
        # Warm incandescent bulb (yellowish-red)
        r = np.clip(r.astype(np.float32) * 1.14, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.88, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])
    elif wb_mode == 2:
        # Cool daylight / blue LED
        b = np.clip(b.astype(np.float32) * 1.12, 0, 255).astype(np.uint8)
        r = np.clip(r.astype(np.float32) * 0.90, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])
    elif wb_mode == 3:
        # Fluorescent light (slightly green-yellow)
        g = np.clip(g.astype(np.float32) * 1.08, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.94, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])
    elif wb_mode == 4:
        # Dim evening light (reduced blue, lower contrast)
        r = np.clip(r.astype(np.float32) * 1.06, 0, 255).astype(np.uint8)
        g = np.clip(g.astype(np.float32) * 1.02, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.85, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])

    # 5. Brightness & Contrast (spanning dark room to bright light)
    brightness_factors = [0.80, 0.92, 1.00, 1.10, 1.22]
    contrast_factors = [0.85, 0.95, 1.00, 1.12, 1.20]
    b_val = brightness_factors[index % len(brightness_factors)]
    c_val = contrast_factors[(index + 2) % len(contrast_factors)]
    aug = np.clip((aug.astype(np.float32) - 128.0) * c_val + 128.0 * b_val, 0, 255).astype(np.uint8)

    # 6. Webcam motion softness / blur
    if index % 4 == 3:
        aug = cv2.GaussianBlur(aug, (3, 3), 0.5)

    # 7. Finger / Thumb holding on edges (simulated hand hold)
    if index % 5 == 4:
        side = index % 2
        cx = int(w * 0.05) if side == 0 else int(w * 0.95)
        cy = int(h * (0.35 + ((index % 3) * 0.15)))
        axes = (int(w * 0.06), int(h * 0.16))
        skin_color = (
            int(115 + (index % 25)),
            int(140 + (index % 25)),
            int(180 + (index % 30))
        )
        cv2.ellipse(aug, (cx, cy), axes, 0, 0, 360, skin_color, -1)
        aug = cv2.GaussianBlur(aug, (3, 3), 0.4)

    return aug


def ingest_all():
    print("=" * 70)
    print("  NoteGuard AI: Ingesting Real User Camera Banknotes Across All Classes")
    print("=" * 70)

    # 1. Extract clean base notes for each denomination
    extracted_bases = {}

    for denom, patterns in USER_CAMERA_SOURCES.items():
        files = []
        for pat in patterns:
            files.extend(glob.glob(pat))
        files = sorted(list(set(files)))
        
        valid_notes = []
        for f in files:
            img = cv2.imread(f)
            if img is None:
                continue
            h, w = img.shape[:2]
            if h < 80 or w < 160:
                continue
            # Crop to note if framed
            cropped, bbox, is_found, meta = quality_checker.detect_and_crop_banknote(img)
            ch, cw = cropped.shape[:2]
            ar = cw / max(1, ch)
            if 1.3 <= ar <= 3.0:
                valid_notes.append(cropped)
            else:
                valid_notes.append(img)

        extracted_bases[denom] = valid_notes
        print(f"[*] Rs_{denom:>4}: Extracted {len(valid_notes)} clean base camera captures.")

        # Save reference crops to dataset/raw/genuine_{denom}_camera
        raw_cam_dir = Path(f"dataset/raw/genuine_{denom}_camera")
        raw_cam_dir.mkdir(parents=True, exist_ok=True)
        for i, note in enumerate(valid_notes[:10]):
            cv2.imwrite(str(raw_cam_dir / f"user_real_{denom}_{i+1:03d}.jpg"), note)

    # 2. Ingest into Authenticity Dataset (genuine)
    print("\n--- Ingesting into Authenticity Dataset ---")
    auth_targets = {
        "train": (Path("dataset/train/genuine"), 70),       # 70 per denom * 8 denoms = 560 samples
        "validation": (Path("dataset/validation/genuine"), 20), # 20 per denom * 8 denoms = 160 samples
        "test": (Path("dataset/test/genuine"), 15)          # 15 per denom * 8 denoms = 120 samples
    }

    # Clean previous camera aug files
    for split_name, (target_path, _) in auth_targets.items():
        for old in target_path.glob("user_cam_*_aug_*.jpg"):
            old.unlink()

    total_auth_added = 0
    for split_name, (target_path, count_per_denom) in auth_targets.items():
        target_path.mkdir(parents=True, exist_ok=True)
        for denom, bases in extracted_bases.items():
            if not bases:
                continue
            for j in range(count_per_denom):
                base_note = bases[j % len(bases)]
                aug = augment_camera_note(base_note, j)
                resized = cv2.resize(aug, (224, 224))
                out_path = target_path / f"user_cam_{denom}_aug_{j+1:03d}.jpg"
                cv2.imwrite(str(out_path), resized)
                total_auth_added += 1

        print(f"[*] Ingested {count_per_denom * len(extracted_bases)} camera samples into {split_name}/genuine")

    # 3. Ingest into Denomination Dataset (train & val)
    print("\n--- Ingesting into Denomination Dataset ---")
    denom_targets = {
        "train": (Path("dataset/denomination/train"), 50),  # 50 camera samples per denom
        "val": (Path("dataset/denomination/val"), 15),     # 15 camera samples per denom
    }

    total_denom_added = 0
    for split_name, (base_target, count_per_denom) in denom_targets.items():
        for denom, bases in extracted_bases.items():
            if not bases:
                continue
            denom_dir = base_target / denom
            denom_dir.mkdir(parents=True, exist_ok=True)
            # Remove old user_cam files in this folder
            for old in denom_dir.glob("user_cam_*_aug_*.jpg"):
                old.unlink()
            for j in range(count_per_denom):
                base_note = bases[j % len(bases)]
                aug = augment_camera_note(base_note, j)
                resized = cv2.resize(aug, (224, 224))
                out_path = denom_dir / f"user_cam_{denom}_aug_{j+1:03d}.jpg"
                cv2.imwrite(str(out_path), resized)
                total_denom_added += 1
        print(f"[*] Ingested {count_per_denom * len(extracted_bases)} camera samples into denomination/{split_name}")

    print(f"\n[+] Total {total_auth_added} Authenticity camera samples ingested.")
    print(f"[+] Total {total_denom_added} Denomination camera samples ingested.")
    print("=" * 70)


if __name__ == "__main__":
    ingest_all()

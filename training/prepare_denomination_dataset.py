"""
NoteGuard AI - Dedicated Denomination Dataset Preparation Pipeline
===================================================================
Curates, standardizes, deduplicates, and splits genuine and reference Indian
currency images across 9 denomination classes:
    ₹5, ₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹1000, ₹2000

Includes:
- Front and Reverse banknote sides (Mahatma Gandhi New and Old Series)
- Stratified 70% Train, 15% Validation, 15% Test split
- Data augmentation for training robustness across camera lighting, angles, and rotations
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import numpy as np

# Denomination classes to support
DENOMINATION_CLASSES = ["5", "10", "20", "50", "100", "200", "500", "1000", "2000"]

def compute_md5(filepath: Path) -> str:
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def collect_source_images() -> Dict[str, List[Path]]:
    """Gathers all verified denomination images across raw and scratch datasets."""
    sources: Dict[str, List[Path]] = {d: [] for d in DENOMINATION_CLASSES}
    seen_hashes = set()

    def add_if_valid(p: Path, denom: str):
        if not p.is_file() or p.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            return
        try:
            h = compute_md5(p)
            if h in seen_hashes:
                return
            img = cv2.imread(str(p))
            if img is None or img.shape[0] < 30 or img.shape[1] < 30:
                return
            seen_hashes.add(h)
            sources[denom].append(p)
        except Exception:
            pass

    # 1. From dataset/raw/genuine
    raw_genuine = Path("dataset/raw/genuine")
    if raw_genuine.exists():
        for p in raw_genuine.glob("*.*"):
            for d in ["2000", "500", "200", "100", "50", "20", "10"]:
                if f"Rs_{d}" in p.name or f"_{d}_" in p.name:
                    add_if_valid(p, d)
                    break

    # 2. From scratch/repo6 comp_data (covers front, back, old, new series)
    comp = Path("scratch/repo6/CNN-based-classification-(PRIMARY)/dataset/comp_data")
    if comp.exists():
        for fldr in comp.iterdir():
            if fldr.is_dir():
                for d in ["2000", "500", "200", "100", "50", "20", "10"]:
                    if fldr.name.startswith(f"{d}_"):
                        for img in fldr.glob("*.*"):
                            add_if_valid(img, d)
                        break

    # 4. From dataset/raw/genuine_5_ref for authentic clean 5 notes
    ref_5 = Path("dataset/raw/genuine_5_ref")
    if ref_5.exists():
        for img in ref_5.glob("*.jpg"):
            add_if_valid(img, "5")

    # 5. From dataset/raw/fake for bogus 1000
    raw_fake = Path("dataset/raw/fake")
    if raw_fake.exists():
        for img in raw_fake.glob("*bogus_1000*.*"):
            add_if_valid(img, "1000")

    # 6. From dataset/raw/genuine_100_camera for authentic camera 100 notes
    ref_100_cam = Path("dataset/raw/genuine_100_camera")
    if ref_100_cam.exists():
        for img in ref_100_cam.glob("*.jpg"):
            add_if_valid(img, "100")

    # 7. From dataset/train/genuine for authentic camera 50 notes
    raw_genuine_train = Path("dataset/train/genuine")
    if raw_genuine_train.exists():
        for img in raw_genuine_train.glob("note_camera_real50_*.*"):
            add_if_valid(img, "50")

    return sources

def augment_image(img_bgr: np.ndarray, index: int) -> np.ndarray:
    """Applies realistic camera, hand occlusion, and illumination augmentations."""
    h, w = img_bgr.shape[:2]
    aug = img_bgr.copy()

    # 1. Perspective / Tilt simulation (±6 degrees)
    if index % 2 == 1:
        d = int(w * 0.04)
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        dx = ((index % 5) - 2) * (d // 2)
        dy = ((index % 4) - 2) * (d // 2)
        pts2 = np.float32([[dx, dy], [w - dx, dy], [-dx, h - dy], [w + dx, h - dy]])
        M_p = cv2.getPerspectiveTransform(pts1, pts2)
        aug = cv2.warpPerspective(aug, M_p, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 2. Rotation (-6 to +6 degrees)
    angle = ((index % 7) - 3) * 2.0
    if angle != 0:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        aug = cv2.warpAffine(aug, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 3. Realistic Room Lighting Gradient
    if index % 3 == 0:
        grad_direction = (index % 4)
        if grad_direction == 0:
            grad = np.tile(np.linspace(0.80, 1.20, w), (h, 1))
        elif grad_direction == 1:
            grad = np.tile(np.linspace(1.20, 0.80, w), (h, 1))
        elif grad_direction == 2:
            grad = np.tile(np.linspace(0.85, 1.15, h), (w, 1)).T
        else:
            grad = np.tile(np.linspace(1.15, 0.85, h), (w, 1)).T
        aug = np.clip(aug.astype(np.float32) * grad[:, :, np.newaxis], 0, 255).astype(np.uint8)

    # 4. Color Temperature / White Balance Shift
    if index % 4 == 1:
        b, g, r = cv2.split(aug)
        r = np.clip(r.astype(np.float32) * 1.10, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.90, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])
    elif index % 4 == 2:
        b, g, r = cv2.split(aug)
        b = np.clip(b.astype(np.float32) * 1.10, 0, 255).astype(np.uint8)
        r = np.clip(r.astype(np.float32) * 0.90, 0, 255).astype(np.uint8)
        aug = cv2.merge([b, g, r])

    # 5. Saturation Jitter (webcam desaturation)
    if index % 3 == 1:
        hsv = cv2.cvtColor(aug, cv2.COLOR_BGR2HSV).astype(np.float32)
        sat_factor = 0.70 + ((index % 5) * 0.12)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * sat_factor, 0, 255)
        aug = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # 6. Overall Brightness & Contrast
    brightness = 0.85 + ((index % 5) * 0.08)
    contrast = 0.90 + ((index % 4) * 0.07)
    aug = np.clip((aug.astype(np.float32) - 128.0) * contrast + 128.0 * brightness, 0, 255).astype(np.uint8)

    # 7. Hand / Finger holding occlusion on borders (simulated user thumbs across all classes)
    if index % 4 == 3:
        side = (index % 2)
        cx = int(w * 0.06) if side == 0 else int(w * 0.94)
        cy = int(h * (0.35 + ((index % 3) * 0.15)))
        axes = (int(w * 0.06), int(h * 0.16))
        skin_color = (
            int(110 + (index % 30)),
            int(135 + (index % 30)),
            int(175 + (index % 35))
        )
        cv2.ellipse(aug, (cx, cy), axes, 0, 0, 360, skin_color, -1)
        cv2.GaussianBlur(aug, (3, 3), 0.5, dst=aug)

    # 8. Subtle webcam motion softness / blur
    if index % 3 == 2:
        aug = cv2.GaussianBlur(aug, (3, 3), 0.5)

    return aug

def build_denomination_dataset(
    output_dir: Path = Path("dataset/denomination"),
    target_size: Tuple[int, int] = (224, 224),
    target_train_per_class: int = 140,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
):
    np.random.seed(seed)
    sources = collect_source_images()

    print("=" * 65)
    print("    NoteGuard AI: Building 9-Class Denomination Dataset    ")
    print("=" * 65)
    for d in DENOMINATION_CLASSES:
        print(f"  ₹{d:>4}: {len(sources[d])} verified physical source images")

    # Clear previous output
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)

    for split in ["train", "validation", "test"]:
        for d in DENOMINATION_CLASSES:
            (output_dir / split / d).mkdir(parents=True, exist_ok=True)

    summary = {split: {d: 0 for d in DENOMINATION_CLASSES} for split in ["train", "validation", "test"]}

    for d, files in sources.items():
        if not files:
            continue
        shuffled = np.random.permutation(files)
        n = len(shuffled)
        n_train = max(1, int(round(n * train_ratio)))
        n_val = max(1, int(round(n * val_ratio)))
        n_test = max(1, n - n_train - n_val)
        if n_train + n_val + n_test > n:
            n_train = max(1, n - n_val - n_test)

        train_files = shuffled[:n_train]
        val_files = shuffled[n_train:n_train + n_val]
        test_files = shuffled[n_train + n_val:]
        if len(test_files) == 0:
            test_files = val_files

        # 1. Validation set (original resized only, no artificial leakage)
        for idx, p in enumerate(val_files):
            img = cv2.imread(str(p))
            if img is not None:
                resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
                out_p = output_dir / "validation" / d / f"val_{d}_{idx:04d}.jpg"
                cv2.imwrite(str(out_p), resized, [cv2.IMWRITE_JPEG_QUALITY, 95])
                summary["validation"][d] += 1

        # 2. Test set (original resized only)
        for idx, p in enumerate(test_files):
            img = cv2.imread(str(p))
            if img is not None:
                resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
                out_p = output_dir / "test" / d / f"test_{d}_{idx:04d}.jpg"
                cv2.imwrite(str(out_p), resized, [cv2.IMWRITE_JPEG_QUALITY, 95])
                summary["test"][d] += 1

        # 3. Train set (original + controlled camera augmentations to balance class representation)
        train_count = 0
        for idx, p in enumerate(train_files):
            img = cv2.imread(str(p))
            if img is not None:
                resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
                out_p = output_dir / "train" / d / f"train_{d}_orig_{idx:04d}.jpg"
                cv2.imwrite(str(out_p), resized, [cv2.IMWRITE_JPEG_QUALITY, 95])
                train_count += 1

        # Balance training partition with domain-specific augmentations
        aug_idx = 0
        while train_count < target_train_per_class:
            src_p = train_files[aug_idx % len(train_files)]
            img = cv2.imread(str(src_p))
            if img is not None:
                aug = augment_image(img, aug_idx)
                resized = cv2.resize(aug, target_size, interpolation=cv2.INTER_AREA)
                out_p = output_dir / "train" / d / f"train_{d}_aug_{aug_idx:04d}.jpg"
                cv2.imwrite(str(out_p), resized, [cv2.IMWRITE_JPEG_QUALITY, 92])
                train_count += 1
            aug_idx += 1
        summary["train"][d] = train_count

    print("\nDataset Build Summary:")
    print("-" * 55)
    print(f"{'Class':<8} | {'Train':<8} | {'Validation':<12} | {'Test':<8}")
    print("-" * 55)
    for d in DENOMINATION_CLASSES:
        print(f"₹{d:<7} | {summary['train'][d]:<8} | {summary['validation'][d]:<12} | {summary['test'][d]:<8}")
    print("-" * 55)
    total_imgs = sum(sum(v.values()) for v in summary.values())
    print(f"[*] Total curated denomination images: {total_imgs}")
    print(f"[*] Dataset successfully built at: {output_dir.resolve()}")

if __name__ == "__main__":
    build_denomination_dataset()

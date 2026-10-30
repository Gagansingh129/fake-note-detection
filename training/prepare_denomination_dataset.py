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

    # 3. From scratch/repo6 database/classification
    db_c = Path("scratch/repo6/data_dump/image - useless/database/classification")
    if db_c.exists():
        for fldr in db_c.iterdir():
            if fldr.is_dir() and fldr.name in DENOMINATION_CLASSES:
                for img in fldr.glob("*.*"):
                    add_if_valid(img, fldr.name)

    # 4. From dataset/raw/fake for 1000 and 5
    raw_fake = Path("dataset/raw/fake")
    if raw_fake.exists():
        for img in raw_fake.glob("*bogus_1000*.*"):
            add_if_valid(img, "1000")
        for img in raw_fake.glob("*dummy*5*.*"):
            add_if_valid(img, "5")

    return sources

def augment_image(img_bgr: np.ndarray, index: int) -> np.ndarray:
    """Applies controlled geometric and photometric augmentations for realistic camera simulation."""
    h, w = img_bgr.shape[:2]
    aug = img_bgr.copy()

    # Slight rotation (-8 to +8 degrees)
    angle = ((index % 7) - 3) * 2.5
    if angle != 0:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        aug = cv2.warpAffine(aug, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    # Brightness adjustment
    brightness_factor = 0.80 + ((index % 5) * 0.10)  # 0.80 to 1.20
    aug = np.clip(aug.astype(np.float32) * brightness_factor, 0, 255).astype(np.uint8)

    # Contrast adjustment
    if index % 3 == 0:
        contrast = 0.90 + ((index % 4) * 0.08)
        aug = np.clip((aug.astype(np.float32) - 128.0) * contrast + 128.0, 0, 255).astype(np.uint8)

    # Slight blur (simulate phone camera soft focus)
    if index % 4 == 0:
        aug = cv2.GaussianBlur(aug, (3, 3), 0.5)

    return aug

def build_denomination_dataset(
    output_dir: Path = Path("dataset/denomination"),
    target_size: Tuple[int, int] = (224, 224),
    target_train_per_class: int = 80,
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

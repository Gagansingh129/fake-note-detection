"""
NoteGuard AI - Dataset Preparation Pipeline
============================================
This script cleans, validates, deduplicates, standardizes, and splits raw Indian
currency note images into Train (70%), Validation (15%), and Test (15%) partitions.

Key Capabilities:
1. Dynamic detection of dataset layout (hierarchical denomination vs flat binary).
2. Verification of file integrity and removal of corrupted/unreadable files.
3. Duplicate image detection using MD5 checksum hashing.
4. Stratified splitting to preserve class ratios while preventing data leakage.
5. Standardized 224x224 image resizing.
6. Comprehensive dataset statistics and class distribution charts.
"""

import os
import sys
import glob
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Valid image extensions
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

def calculate_md5(file_path: Path) -> str:
    """Calculate MD5 checksum of a file to identify exact duplicate images."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_image(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Check if an image can be successfully opened and decoded.
    Returns (is_valid, error_reason).
    """
    if file_path.suffix.lower() not in VALID_EXTENSIONS:
        return False, f"Unsupported extension: {file_path.suffix}"
    
    if file_path.stat().st_size == 0:
        return False, "File is 0 bytes (empty)"
        
    try:
        img = cv2.imread(str(file_path))
        if img is None:
            return False, "cv2.imread failed to decode image"
        if len(img.shape) != 3 or img.shape[2] != 3:
            return False, f"Expected 3 channels (RGB/BGR), found shape {img.shape}"
        if img.shape[0] < 32 or img.shape[1] < 32:
            return False, f"Image resolution too low ({img.shape[1]}x{img.shape[0]})"
        return True, None
    except Exception as e:
        return False, str(e)

def discover_dataset(raw_dir: Path) -> Tuple[str, List[Dict]]:
    """
    Automatically detects dataset structure:
    Type 1: Hierarchical: raw/<denomination>/<authenticity>/image.jpg
    Type 2: Flat binary: raw/<authenticity>/image.jpg
    """
    samples = []
    subdirs = [d for d in raw_dir.iterdir() if d.is_dir()]
    if not subdirs:
        return "empty", []

    # Check if subdirs contain authenticity subfolders (e.g., 100/genuine, 500/fake)
    has_nested_auth = False
    for d in subdirs:
        inner_dirs = [sd.name.lower() for sd in d.iterdir() if sd.is_dir()]
        if any(auth in inner_dirs for auth in ['genuine', 'fake', 'real']):
            has_nested_auth = True
            break

    if has_nested_auth:
        mode = "hierarchical"
        for denom_dir in subdirs:
            denom = denom_dir.name
            for auth_dir in denom_dir.iterdir():
                if not auth_dir.is_dir():
                    continue
                auth = "genuine" if "genuine" in auth_dir.name.lower() or "real" in auth_dir.name.lower() else "fake"
                for img_file in auth_dir.glob("*.*"):
                    if img_file.is_file() and img_file.name != ".gitkeep":
                        samples.append({
                            "path": img_file,
                            "denomination": denom,
                            "authenticity": auth,
                            "class_id": f"{denom}_{auth}"
                        })
    else:
        # Check flat binary structure
        mode = "flat_binary"
        for auth_dir in subdirs:
            auth_name = auth_dir.name.lower()
            if "genuine" in auth_name or "real" in auth_name:
                auth = "genuine"
            elif "fake" in auth_name or "counterfeit" in auth_name:
                auth = "fake"
            else:
                auth = auth_name
            for img_file in auth_dir.glob("*.*"):
                if img_file.is_file() and img_file.name != ".gitkeep":
                    samples.append({
                        "path": img_file,
                        "denomination": "unknown",
                        "authenticity": auth,
                        "class_id": auth
                    })

    return mode, samples

def split_dataset(
    samples: List[Dict],
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
) -> Dict[str, List[Dict]]:
    """
    Performs stratified split ensuring:
    1. Equal class distribution in Train, Validation, and Test.
    2. Reproducibility using fixed random seed.
    3. No data leakage.
    """
    np.random.seed(seed)
    
    # Group samples by class_id
    grouped: Dict[str, List[Dict]] = {}
    for sample in samples:
        grouped.setdefault(sample["class_id"], []).append(sample)

    splits = {"train": [], "validation": [], "test": []}

    for class_id, class_samples in grouped.items():
        # Shuffle deterministically
        indices = np.random.permutation(len(class_samples))
        n = len(class_samples)
        
        n_train = int(round(train_ratio * n))
        n_val = int(round(val_ratio * n))
        
        # Ensure at least 1 sample per split if sample size allows
        if n >= 3:
            n_train = max(1, min(n - 2, n_train))
            n_val = max(1, min(n - n_train - 1, n_val))
        elif n == 2:
            n_train, n_val = 1, 0
        else:
            n_train, n_val = 1, 0

        train_idx = indices[:n_train]
        val_idx = indices[n_train:n_train + n_val]
        test_idx = indices[n_train + n_val:]

        for i in train_idx:
            splits["train"].append(class_samples[i])
        for i in val_idx:
            splits["validation"].append(class_samples[i])
        for i in test_idx:
            splits["test"].append(class_samples[i])

    return splits

def process_and_save(
    splits: Dict[str, List[Dict]],
    output_base: Path,
    image_size: Tuple[int, int] = (224, 224),
    mode: str = "hierarchical"
) -> Dict:
    """
    Resizes images, normalizes dimensions, and stores them in train/val/test folders.
    """
    stats = {
        "train": 0,
        "validation": 0,
        "test": 0,
        "by_class": {},
        "by_denomination": {},
        "by_authenticity": {"genuine": 0, "fake": 0}
    }

    for split_name, split_samples in splits.items():
        for item in split_samples:
            src_path = item["path"]
            denom = item["denomination"]
            auth = item["authenticity"]

            # Target directory
            if mode == "hierarchical":
                target_dir = output_base / split_name / denom / auth
            else:
                target_dir = output_base / split_name / auth
            target_dir.mkdir(parents=True, exist_ok=True)

            target_path = target_dir / f"{src_path.stem}.jpg"

            # Read, resize, and write
            img = cv2.imread(str(src_path))
            if img is not None:
                img_resized = cv2.resize(img, image_size, interpolation=cv2.INTER_AREA)
                cv2.imwrite(str(target_path), img_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                
                stats[split_name] += 1
                class_key = f"{split_name}:{item['class_id']}"
                stats["by_class"][class_key] = stats["by_class"].get(class_key, 0) + 1
                
                stats["by_denomination"][denom] = stats["by_denomination"].get(denom, 0) + 1
                stats["by_authenticity"][auth] = stats["by_authenticity"].get(auth, 0) + 1

    return stats

def plot_dataset_statistics(stats: Dict, output_path: Path):
    """Generate a clean visual chart of the dataset split and class distribution."""
    plt.figure(figsize=(10, 5))
    
    # Subplot 1: Split Distribution
    plt.subplot(1, 2, 1)
    split_names = ['Train (70%)', 'Validation (15%)', 'Test (15%)']
    counts = [stats['train'], stats['validation'], stats['test']]
    colors = ['#2563eb', '#10b981', '#f59e0b']
    
    bars = plt.bar(split_names, counts, color=colors, edgecolor='black', alpha=0.85)
    plt.title('Dataset Split Distribution', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Images', fontsize=10)
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., h + max(1, h*0.02),
                 f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Subplot 2: Authenticity Distribution
    plt.subplot(1, 2, 2)
    auth_names = list(stats['by_authenticity'].keys())
    auth_counts = [stats['by_authenticity'][k] for k in auth_names]
    auth_colors = ['#10b981', '#ef4444'] if 'genuine' in auth_names else ['#6b7280', '#3b82f6']
    
    bars_auth = plt.bar([k.capitalize() for k in auth_names], auth_counts, color=auth_colors, edgecolor='black', alpha=0.85)
    plt.title('Authenticity Distribution (Total)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Images', fontsize=10)
    for bar in bars_auth:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., h + max(1, h*0.02),
                 f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"[*] Distribution chart saved to: {output_path}")

def generate_mock_dataset(raw_dir: Path, notes_per_class: int = 12):
    """
    Creates mock test dataset placeholders (labeled synthetic geometric frames)
    for pipeline verification and automated testing when raw photos are not yet placed.
    Does NOT generate counterfeit images; generates labeled calibration cards.
    """
    print("[!] Generating mock test cards for pipeline verification...")
    denominations = ["100", "200", "500"]
    labels = ["genuine", "fake"]

    for denom in denominations:
        for auth in labels:
            folder = raw_dir / denom / auth
            folder.mkdir(parents=True, exist_ok=True)
            for i in range(notes_per_class):
                # Create a standardized test card with text
                card = np.full((300, 600, 3), 240 if auth == "genuine" else 220, dtype=np.uint8)
                # Draw border
                color = (40, 140, 40) if auth == "genuine" else (40, 40, 180)
                cv2.rectangle(card, (15, 15), (585, 285), color, 4)
                # Draw denomination and watermark simulator circle
                cv2.circle(card, (120, 150), 60, (200, 200, 200), -1)
                cv2.putText(card, f"INR {denom}", (240, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3)
                cv2.putText(card, f"SAMPLE: {auth.upper()} #{i+1}", (240, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 80), 2)
                
                file_path = folder / f"note_{denom}_{auth}_{i+1:03d}.jpg"
                cv2.imwrite(str(file_path), card)
    print(f"[*] Generated {len(denominations) * len(labels) * notes_per_class} mock samples across denominations in {raw_dir}")

def run_preparation(raw_dir_str: str, dataset_root_str: str, seed: int = 42, generate_mock: bool = False):
    """Main execution flow for dataset cleaning, validation, and splitting."""
    raw_dir = Path(raw_dir_str)
    dataset_root = Path(dataset_root_str)

    print("=" * 65)
    print("      NoteGuard AI - Dataset Preparation & Cleaning Pipeline      ")
    print("=" * 65)

    mode, samples = discover_dataset(raw_dir)
    
    if mode == "empty" or len(samples) == 0:
        if generate_mock:
            generate_mock_dataset(raw_dir)
            mode, samples = discover_dataset(raw_dir)
        else:
            print(f"\n[!] Notice: No valid images found in {raw_dir}.")
            print("    Please place your dataset inside dataset/raw/ following:")
            print("    dataset/raw/<denomination>/<genuine|fake>/<image.jpg>")
            print("    or run with '--generate-mock' for automated pipeline verification.\n")
            return

    print(f"[*] Discovered layout mode: {mode}")
    print(f"[*] Initial raw image files found: {len(samples)}")

    # Step 1: Verification & Corrupted file detection
    valid_samples = []
    corrupted_files = []
    for s in samples:
        is_valid, reason = verify_image(s["path"])
        if is_valid:
            valid_samples.append(s)
        else:
            corrupted_files.append((s["path"], reason))

    if corrupted_files:
        print(f"[!] Warning: {len(corrupted_files)} corrupted/invalid files flagged:")
        for p, r in corrupted_files[:5]:
            print(f"    - {p.name}: {r}")

    # Step 2: Deduplication using MD5
    seen_hashes = {}
    unique_samples = []
    duplicate_count = 0
    for s in valid_samples:
        file_hash = calculate_md5(s["path"])
        if file_hash in seen_hashes:
            duplicate_count += 1
        else:
            seen_hashes[file_hash] = s["path"]
            unique_samples.append(s)

    print(f"[*] Total valid images: {len(valid_samples)}")
    print(f"[*] Duplicate images removed: {duplicate_count}")
    print(f"[*] Unique curated images: {len(unique_samples)}")

    # Step 3: Stratified 70/15/15 Split
    splits = split_dataset(unique_samples, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=seed)
    print(f"[*] Split counts -> Train: {len(splits['train'])} | Val: {len(splits['validation'])} | Test: {len(splits['test'])}")

    # Step 4: Standardization (224x224) and Export
    stats = process_and_save(splits, dataset_root, image_size=(224, 224), mode=mode)
    
    # Save statistics JSON
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    report_file = results_dir / "dataset_statistics.json"
    with open(report_file, "w") as f:
        json.dump(stats, f, indent=4)
    print(f"[*] Dataset report saved to: {report_file}")

    # Generate visual charts
    plot_path = results_dir / "graphs" / "dataset_distribution.png"
    plot_dataset_statistics(stats, plot_path)

    print("=" * 65)
    print("Dataset Preparation Completed Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare NoteGuard AI Dataset")
    parser.add_argument("--raw-dir", type=str, default="dataset/raw", help="Path to raw dataset")
    parser.add_argument("--dataset-root", type=str, default="dataset", help="Output directory for train/val/test")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible split")
    parser.add_argument("--generate-mock", action="store_true", help="Generate mock calibration dataset if empty")
    args = parser.parse_args()

    run_preparation(args.raw_dir, args.dataset_root, args.seed, args.generate_mock)

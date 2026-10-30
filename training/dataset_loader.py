"""
NoteGuard AI - Dataset Loader & Preprocessing Utilities
======================================================
Loads image datasets with tf.data pipelines, dynamic class extraction,
automatic class weighting for imbalanced data, and augmentation integration.
"""

import os
import json
from pathlib import Path
from typing import Tuple, Dict, List, Optional
import numpy as np
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight

def get_class_names_and_paths(
    dataset_dir: Path,
    task: str = "authenticity"
) -> Tuple[List[str], List[Tuple[str, int]]]:
    """
    Extracts file paths and integer labels depending on the task:
    - task='authenticity': extracts 'genuine' (0) vs 'fake' (1)
    - task='denomination': extracts denomination folders (e.g. '100', '200', '500')
    """
    file_records = []
    classes = set()

    for img_path in dataset_dir.glob("**/*.jpg"):
        parts = [p.lower() for p in img_path.parts]
        
        if task == "authenticity":
            if "genuine" in parts:
                label_name = "genuine"
            elif "fake" in parts:
                label_name = "fake"
            else:
                label_name = img_path.parent.name.lower()
            classes.add(label_name)
            file_records.append((str(img_path), label_name))
        else: # denomination
            import re
            found_denom = None
            # Check parent folder names first (exclude filename)
            for p in img_path.parts[:-1]:
                clean_p = p.replace("Rs_", "").replace("rs_", "")
                if clean_p in ["10", "20", "50", "100", "200", "500", "2000"]:
                    found_denom = f"Rs_{clean_p}"
                    break

            # Check explicit tokens in filename
            if not found_denom:
                # 1. Explicit Rs_X token (e.g. note_denom_Rs_100_... or Rs_500_...)
                m = re.search(r'(?:^|[_\/\\])Rs_(2000|500|200|100|50|20|10)(?:[_\/\.\\]|$)', img_path.name, re.IGNORECASE)
                if m:
                    found_denom = f"Rs_{m.group(1)}"
                else:
                    # 2. Starts with note_X_
                    m2 = re.search(r'^note_(2000|500|200|100|50|20|10)_', img_path.name, re.IGNORECASE)
                    if m2:
                        found_denom = f"Rs_{m2.group(1)}"
                    elif "fake_alphabet_in_serial" in img_path.name:
                        found_denom = "Rs_100"

            # When evaluating or training denomination, only keep verified denominations
            if found_denom:
                label_name = found_denom
                classes.add(label_name)
                file_records.append((str(img_path), label_name))

    class_names = sorted(list(classes))
    label_map = {name: idx for idx, name in enumerate(class_names)}
    labeled_files = [(path, label_map[name]) for path, name in file_records]

    return class_names, labeled_files


def load_dataset_tf(
    dataset_dir: str,
    task: str = "authenticity",
    image_size: Tuple[int, int] = (224, 224),
    batch_size: int = 16,
    is_training: bool = False,
    normalization: str = "rescaling"
) -> Tuple[tf.data.Dataset, List[str], Optional[Dict[int, float]]]:
    """
    Creates an optimized tf.data.Dataset with prefetching, parallel loading,
    and optional training-only augmentation.
    """
    path = Path(dataset_dir)
    if not path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    class_names, labeled_files = get_class_names_and_paths(path, task=task)
    if not labeled_files:
        raise ValueError(f"No valid images found in {dataset_dir} for task '{task}'.")

    paths = [f[0] for f in labeled_files]
    labels = [f[1] for f in labeled_files]

    # Calculate class weights for training
    class_weights = None
    if is_training and len(set(labels)) > 1:
        weights = compute_class_weight(
            class_weight="balanced",
            classes=np.unique(labels),
            y=np.array(labels)
        )
        class_weights = {int(cls): float(round(w, 4)) for cls, w in zip(np.unique(labels), weights)}

    def parse_image(file_path, label):
        img = tf.io.read_file(file_path)
        img = tf.io.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, image_size)
        
        if normalization == "rescaling":
            img = img / 255.0
        elif normalization == "efficientnet":
            img = tf.keras.applications.efficientnet.preprocess_input(img)
        elif normalization == "mobilenet":
            img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
            
        return img, label

    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))
    if is_training:
        dataset = dataset.shuffle(buffer_size=len(paths), reshuffle_each_iteration=True)

    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)

    # Apply training augmentation if training
    if is_training:
        from app.services.preprocessing import get_training_augmentation_pipeline
        aug = get_training_augmentation_pipeline()
        dataset = dataset.map(lambda x, y: (aug(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)

    dataset = dataset.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)

    return dataset, class_names, class_weights

import os, sys
sys.path.append(os.getcwd())
from pathlib import Path
from training.dataset_loader import get_class_names_and_paths
from collections import Counter

train_classes, train_files = get_class_names_and_paths(Path("dataset/train"), task="denomination")
print("Train Classes:", train_classes)
print("Total train files:", len(train_files))
tc = Counter([f[1] for f in train_files])
for idx, name in enumerate(train_classes):
    print(f"  {name:8}: {tc[idx]} files")

val_classes, val_files = get_class_names_and_paths(Path("dataset/validation"), task="denomination")
print("\nVal Classes:", val_classes)
print("Total val files:", len(val_files))
vc = Counter([f[1] for f in val_files])
for idx, name in enumerate(val_classes):
    print(f"  {name:8}: {vc[idx]} files")

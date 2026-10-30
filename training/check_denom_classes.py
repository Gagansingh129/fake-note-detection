import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from training.dataset_loader import get_class_names_and_paths
from collections import Counter

classes, files = get_class_names_and_paths(Path("dataset/train"), task="denomination")
print("Train Classes:", classes)
print("Total train files:", len(files))
c = Counter([f[1] for f in files])
print("Distribution:", {classes[k]: v for k, v in c.items()})

val_classes, val_files = get_class_names_and_paths(Path("dataset/validation"), task="denomination")
print("\nVal Classes:", val_classes)
print("Total val files:", len(val_files))
vc = Counter([f[1] for f in val_files])
print("Distribution:", {val_classes[k]: v for k, v in vc.items()})

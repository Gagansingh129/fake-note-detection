import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))
from training.dataset_loader import get_class_names_and_paths
from collections import Counter

classes, files = get_class_names_and_paths(Path('dataset/train'), task='denomination')
counts = Counter([c for _, c in files])
print('Discovered Classes:', classes)
print('Training Counts:', {classes[k]: v for k, v in counts.items()})

val_classes, val_files = get_class_names_and_paths(Path('dataset/validation'), task='denomination')
val_counts = Counter([c for _, c in val_files])
print('Validation Counts:', {val_classes[k]: v for k, v in val_counts.items()})

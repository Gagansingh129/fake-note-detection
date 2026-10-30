import os, sys
sys.path.append(os.getcwd())
from pathlib import Path
from training.dataset_loader import get_class_names_and_paths

class_names, files = get_class_names_and_paths(Path("dataset/train"), task="denomination")
print("Classes:", class_names)

files_50 = [f[0] for f in files if class_names[f[1]] == "Rs_50"]
files_100 = [f[0] for f in files if class_names[f[1]] == "Rs_100"]

print(f"Total Rs_50 files: {len(files_50)}")
print("Sample Rs_50 files (first 5):")
for f in files_50[:5]:
    print(" ", Path(f).name)

print(f"\nTotal Rs_100 files: {len(files_100)}")
print("Sample Rs_100 files (first 5):")
for f in files_100[:5]:
    print(" ", Path(f).name)

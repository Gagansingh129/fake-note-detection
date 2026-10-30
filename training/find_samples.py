from pathlib import Path

print("Uploads:")
for p in list(Path("backend/static/uploads").glob("*.jpg"))[:5]:
    print(" ", p)

print("Dummy files in dataset:")
for p in list(Path("dataset").glob("**/*dummy*"))[:5]:
    print(" ", p)

print("Denominations:")
for d in ['Rs_10', 'Rs_20', 'Rs_50', 'Rs_100', 'Rs_200', 'Rs_500', 'Rs_2000']:
    found = list(Path("dataset").glob(f"**/*{d}*"))[:1]
    if found:
        print(f"  {d}: {found[0]}")

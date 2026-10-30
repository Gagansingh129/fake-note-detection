from pathlib import Path

print("Looking for 100 notes in dataset:")
for p in Path("dataset").glob("**/*100*.jpg"):
    print(p)
    if "fake" in str(p):
        print("  ^^ fake 100")

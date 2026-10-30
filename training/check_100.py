import cv2

p_fake = "dataset/train/100/fake/note_100_fake_001.jpg"
p_gen = "dataset/train/100/genuine/note_100_genuine_001.jpg"

img_f = cv2.imread(p_fake)
img_g = cv2.imread(p_gen)

print("Fake 100 shape:", img_f.shape if img_f is not None else None)
print("Genuine 100 shape:", img_g.shape if img_g is not None else None)

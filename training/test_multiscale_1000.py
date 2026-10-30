import cv2
import numpy as np

def detect_1000_numeral(img_bgr, tpl_bgr):
    """
    Performs multi-scale correlation matching to detect if the banknote
    displays the bogus/fantasy ₹1000 numeral.
    """
    gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray_tpl = cv2.cvtColor(tpl_bgr, cv2.COLOR_BGR2GRAY)
    th, tw = gray_tpl.shape[:2]

    # Search in right-center region where denomination is printed
    h, w = gray_img.shape[:2]
    search_roi = gray_img[int(h * 0.40):int(h * 0.90), int(w * 0.55):int(w * 0.95)]
    sh, sw = search_roi.shape[:2]

    best_score = 0.0
    for scale in np.linspace(0.7, 1.4, 8):
        scaled_w = int(tw * scale)
        scaled_h = int(th * scale)
        if scaled_h >= sh or scaled_w >= sw:
            continue
        resized_tpl = cv2.resize(gray_tpl, (scaled_w, scaled_h))
        res = cv2.matchTemplate(search_roi, resized_tpl, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, _ = cv2.minMaxLoc(res)
        if max_v > best_score:
            best_score = max_v

    return best_score >= 0.65, best_score

# Test on bogus note
bogus_img = cv2.imread("backend/uploads/user_camera_bogus_note.jpg")
tpl = cv2.imread("backend/uploads/template_1000.png")
is_1000, score = detect_1000_numeral(bogus_img, tpl)
print(f"Bogus Note: is_1000 = {is_1000} (score = {score:.4f})")

# Test on real 2000, 500, 100, 50
for p in ["dataset/raw/genuine/note_2000_Rs_2000_0129.jpg", "dataset/raw/genuine/note_500_Rs_500_0120.jpg", "dataset/test/genuine/note_denom_Rs_50_Rs_50_0200.jpg"]:
    g_img = cv2.imread(p)
    if g_img is not None:
        g_is, g_sc = detect_1000_numeral(g_img, tpl)
        print(f"Genuine ({p[:30]}): is_1000 = {g_is} (score = {g_sc:.4f})")

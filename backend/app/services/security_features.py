"""
NoteGuard AI - Computer Vision Security Feature Analysis Service
================================================================
Performs objective OpenCV-based structural, geometric, and texture checks
on Indian currency notes as supporting evidence for deep learning screening.

IMPORTANT FORENSIC PRINCIPLE:
Computer vision checks operate on standard visible-light RGB images.
Features requiring transmitted backlighting (watermark), 365nm UV light,
or optical magnification (micro-lettering) cannot be definitively verified
via camera and are explicitly flagged as unavailable.
"""

from typing import Dict, Any, Tuple
from pathlib import Path
import cv2
import numpy as np


# Standard physical dimensions (mm) and aspect ratios for Indian currency notes
# (Mahatma Gandhi New Series)
CURRENCY_DIMENSIONS = {
    "10": {"length_mm": 123, "width_mm": 63, "aspect": 1.95, "color_family": "Chocolate Brown"},
    "20": {"length_mm": 129, "width_mm": 63, "aspect": 2.05, "color_family": "Greenish Yellow"},
    "50": {"length_mm": 135, "width_mm": 66, "aspect": 2.05, "color_family": "Fluorescent Blue"},
    "100": {"length_mm": 142, "width_mm": 66, "aspect": 2.15, "color_family": "Lavender"},
    "200": {"length_mm": 146, "width_mm": 66, "aspect": 2.21, "color_family": "Bright Yellow"},
    "500": {"length_mm": 150, "width_mm": 66, "aspect": 2.27, "color_family": "Stone Grey"},
    "1000": {"length_mm": 150, "width_mm": 66, "aspect": 2.27, "color_family": "Non-existent Bogus / Illegal Tender"},
    "2000": {"length_mm": 166, "width_mm": 66, "aspect": 2.51, "color_family": "Magenta"},
}


def check_for_bogus_1000_numeral(img_bgr: np.ndarray) -> Tuple[bool, float]:
    """
    Checks if the note displays a bogus ₹1000 denomination numeral.
    Since ₹1000 was demonetized in 2016 and never issued in the New Series design,
    any modern ₹1000 banknote is an unauthorized counterfeit reproduction.
    """
    tpl_path = Path(__file__).resolve().parent.parent / "models" / "template_1000.png"
    if not tpl_path.exists():
        tpl_path = Path(__file__).resolve().parent.parent.parent / "models" / "template_1000.png"
    if not tpl_path.exists():
        return False, 0.0

    tpl_bgr = cv2.imread(str(tpl_path))
    if tpl_bgr is None:
        return False, 0.0

    gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray_tpl = cv2.cvtColor(tpl_bgr, cv2.COLOR_BGR2GRAY)
    th, tw = gray_tpl.shape[:2]

    h, w = gray_img.shape[:2]
    # Denomination numeral zone: right-center
    search_roi = gray_img[int(h * 0.40):int(h * 0.90), int(w * 0.55):int(w * 0.95)]
    sh, sw = search_roi.shape[:2]

    best_score = 0.0
    for scale in np.linspace(0.65, 1.45, 9):
        scaled_w = int(tw * scale)
        scaled_h = int(th * scale)
        if scaled_h >= sh or scaled_w >= sw or scaled_h < 10 or scaled_w < 10:
            continue
        resized_tpl = cv2.resize(gray_tpl, (scaled_w, scaled_h))
        res = cv2.matchTemplate(search_roi, resized_tpl, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, _ = cv2.minMaxLoc(res)
        if max_v > best_score:
            best_score = float(max_v)

    return best_score >= 0.65, round(best_score, 4)


def check_for_100_numeral(img_bgr: np.ndarray) -> Tuple[bool, float]:
    """
    Checks if the note displays a 100 denomination numeral
    (e.g. on Mahatma Gandhi old/new 100 notes).
    """
    tpl_path = Path(__file__).resolve().parent.parent / "models" / "template_100.png"
    if not tpl_path.exists():
        tpl_path = Path(__file__).resolve().parent.parent.parent / "models" / "template_100.png"
    if not tpl_path.exists():
        return False, 0.0

    tpl_bgr = cv2.imread(str(tpl_path))
    if tpl_bgr is None:
        return False, 0.0

    gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray_tpl = cv2.cvtColor(tpl_bgr, cv2.COLOR_BGR2GRAY)
    th, tw = gray_tpl.shape[:2]

    h, w = gray_img.shape[:2]
    search_roi = gray_img[int(h * 0.10):int(h * 0.70), int(w * 0.30):int(w * 0.75)]
    sh, sw = search_roi.shape[:2]

    best_score = 0.0
    for scale in np.linspace(0.65, 1.45, 9):
        scaled_w = int(tw * scale)
        scaled_h = int(th * scale)
        if scaled_h >= sh or scaled_w >= sw or scaled_h < 10 or scaled_w < 10:
            continue
        resized_tpl = cv2.resize(gray_tpl, (scaled_w, scaled_h))
        res = cv2.matchTemplate(search_roi, resized_tpl, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, _ = cv2.minMaxLoc(res)
        if max_v > best_score:
            best_score = float(max_v)

    return best_score >= 0.60, round(best_score, 4)


def analyze_banknote_security_features(
    image_bgr: np.ndarray,
    denomination_str: str = "₹500"
) -> Dict[str, Any]:
    """
    Performs visible-light OpenCV security checks:
    1. Aspect Ratio & Geometric Consistency
    2. Security Thread Region Edge Analysis
    3. Micro-Texture & Print Crispness Analysis
    4. Portrait Region Contrast Analysis
    5. Equipment-Dependent Physical Checks (Reported as Unavailable)
    """
    h, w = image_bgr.shape[:2]
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    denom_clean = denomination_str.replace("₹", "").replace("Rs_", "").strip()

    # 1. Aspect Ratio & Dimensions
    current_aspect = round(float(w) / h, 2) if h > 0 else 1.0
    expected_info = CURRENCY_DIMENSIONS.get(denom_clean, {"aspect": 2.15, "color_family": "Standard"})
    expected_aspect = expected_info["aspect"]
    
    # Aspect ratio error tolerance
    aspect_diff = abs(current_aspect - expected_aspect)
    aspect_consistent = aspect_diff <= 0.40  # Allow some perspective tilt

    # 2. Security Thread Region Analysis (Window at ~30% - 40% from left)
    # Authentic notes have an embedded windowed security thread with high vertical gradient
    x_start = int(w * 0.28)
    x_end = int(w * 0.42)
    thread_roi = gray[:, x_start:x_end] if x_end > x_start else gray
    
    sobel_x = cv2.Sobel(thread_roi, cv2.CV_64F, 1, 0, ksize=3)
    thread_gradient = float(np.mean(np.abs(sobel_x)))
    # High-contrast vertical edge boundaries indicate presence of thread strip
    thread_detected = thread_gradient >= 14.0

    # 3. Micro-Texture & Print Sharpness Analysis (Center region)
    cx0, cx1 = int(w * 0.25), int(w * 0.75)
    cy0, cy1 = int(h * 0.20), int(h * 0.80)
    center_roi = gray[cy0:cy1, cx0:cx1] if (cx1 > cx0 and cy1 > cy0) else gray
    
    laplacian_var = float(cv2.Laplacian(center_roi, cv2.CV_64F).var())
    print_crisp = laplacian_var >= 45.0

    # 4. Portrait Region Contrast (Typically right-center at 60% - 85% width)
    px0, px1 = int(w * 0.58), int(w * 0.88)
    py0, py1 = int(h * 0.15), int(h * 0.85)
    portrait_roi = gray[py0:py1, px0:px1] if (px1 > px0 and py1 > py0) else gray
    
    portrait_contrast = float(np.std(portrait_roi))
    portrait_contrast_pass = portrait_contrast >= 25.0

    # 5. Dummy / Toy Note Anomaly Screening (Full of Fun, Children Bank, Coupon notes)
    right_edge_roi = image_bgr[:, int(w * 0.86):]
    hsv_right = cv2.cvtColor(right_edge_roi, cv2.COLOR_BGR2HSV)
    coupon_color_mask = cv2.inRange(hsv_right, np.array([8, 100, 100]), np.array([35, 255, 255]))
    coupon_ratio = float(np.mean(coupon_color_mask > 0))
    has_toy_coupon_banner = coupon_ratio > 0.14

    thread_bgr = image_bgr[:, x_start:x_end]
    red_diff = thread_bgr[:, :, 2].astype(float) - thread_bgr[:, :, 1].astype(float)
    has_red_fake_thread = float(np.mean(red_diff)) > 42.0

    mean_b, mean_g, mean_r = np.mean(image_bgr, axis=(0, 1))
    color_anomaly = False
    if denom_clean == "10" and (mean_b > 130 and mean_g > 145 and mean_r > 170):
        color_anomaly = True

    dummy_note_flag = has_toy_coupon_banner or (has_red_fake_thread and color_anomaly)

    # Check for Bogus / Fantasy ₹1000 Numeral
    is_bogus_1000, bogus_score = check_for_bogus_1000_numeral(image_bgr)

    # Composite Supporting Score (0.0 to 1.0)
    score_components = [
        1.0 if aspect_consistent else 0.4,
        1.0 if thread_detected and not has_red_fake_thread else 0.3,
        1.0 if print_crisp else 0.4,
        1.0 if portrait_contrast_pass else 0.4,
        0.1 if dummy_note_flag or is_bogus_1000 else 1.0,
    ]
    cv_support_score = round(float(np.mean(score_components)), 3)

    return {
        "aspect_ratio": {
            "measured": current_aspect,
            "expected_reference": expected_aspect,
            "status": "Consistent" if aspect_consistent else "Non-Standard Dimension",
            "is_valid": aspect_consistent
        },
        "bogus_denomination_1000": {
            "detected": is_bogus_1000,
            "confidence_score": bogus_score,
            "status": "Bogus ₹1000 Numeral Detected" if is_bogus_1000 else "Standard Legal Tender Numeral",
            "is_valid": not is_bogus_1000,
            "warning": "₹1000 was demonetized in 2016 and never reissued in the Mahatma Gandhi New Series. This note is counterfeit." if is_bogus_1000 else None
        },
        "security_thread": {
            "evaluated_region": "28%-42% horizontal width",
            "edge_gradient_intensity": round(thread_gradient, 2),
            "status": "Visible Continuous / Windowed Pattern" if (thread_detected and not has_red_fake_thread) else (
                "Artificial / Colored Line Profile (Toy Marker)" if has_red_fake_thread else "Indistinct or Missing Thread Profile"
            ),
            "is_valid": thread_detected and not has_red_fake_thread,
            "note": "Evaluates visible surface pattern only. Fluorescent and magnetic thread verification requires lab hardware."
        },
        "print_texture": {
            "micro_texture_variance": round(laplacian_var, 2),
            "status": "Crisp Intaglio / Relief Print Quality" if print_crisp else "Soft / Uniform Dither Texture (Potential Mockup/Copy)",
            "is_valid": print_crisp
        },
        "portrait_contrast": {
            "contrast_variance": round(portrait_contrast, 2),
            "status": "Adequate Dynamic Range" if portrait_contrast_pass else "Low Contrast in Portrait Zone",
            "is_valid": portrait_contrast_pass
        },
        "dummy_currency_markers": {
            "detected": dummy_note_flag,
            "has_coupon_banner": has_toy_coupon_banner,
            "has_colored_fake_thread": has_red_fake_thread,
            "color_scheme_anomaly": color_anomaly,
            "status": "Toy / Dummy Note Pattern Detected (Coupon Label / Full of Fun)" if dummy_note_flag else "No Obvious Toy Markers"
        },
        "physical_features_unavailable_on_camera": [
            {
                "feature": "Mahatma Gandhi Watermark (Transmitted Light)",
                "status": "Unavailable",
                "reason": "Requires transmitted backlighting through the banknote paper; surface cameras only capture reflected light."
            },
            {
                "feature": "UV Fluorescent Fibres & Optical Ink",
                "status": "Unavailable",
                "reason": "Requires specialized 365nm Ultraviolet illumination source."
            },
            {
                "feature": "Intaglio Micro-Lettering ('RBI' / Denomination)",
                "status": "Unavailable",
                "reason": "Requires optical macro magnification lens (>= 10x)."
            },
            {
                "feature": "Latent Denomination Image",
                "status": "Unavailable",
                "reason": "Requires variable tilt inspection at eye-level 45-degree angle."
            }
        ],
        "cv_support_score": cv_support_score,
        "disclaimer": "Computer vision checks provide supporting morphological evidence. They do not constitute official banking authentication."
    }

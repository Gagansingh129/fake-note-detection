"""
NoteGuard AI - Image Processing & Quality Assessment Service
============================================================
Evaluates raw note images for blur, ambient illumination, glare, and resolution
before sending them to deep learning inference.
"""

from typing import Dict, Any, Tuple
import cv2
import numpy as np


class ImageQualityChecker:
    """
    Automated pre-screening quality checker.
    Prevents false counterfeit classifications caused by blurred cameras,
    dark rooms, or excessive flash reflection.
    """

    def __init__(
        self,
        min_resolution: Tuple[int, int] = (180, 180),
        min_blur_score: float = 60.0,
        min_brightness: float = 0.22,
        max_brightness: float = 0.92,
        max_glare_ratio: float = 0.20
    ):
        self.min_resolution = min_resolution
        self.min_blur_score = min_blur_score
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
        self.max_glare_ratio = max_glare_ratio

    def calculate_blur(self, image_bgr: np.ndarray) -> float:
        """
        Calculates sharpness using the Variance of Laplacian method.
        A higher variance means sharp edges. Low variance means blurry image.
        """
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return float(round(laplacian_var, 2))

    def calculate_brightness(self, image_bgr: np.ndarray) -> float:
        """
        Calculates average image brightness normalized between 0.0 (pitch black)
        and 1.0 (pure white) using the Value channel in HSV.
        """
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]
        mean_brightness = float(np.mean(v_channel) / 255.0)
        return float(round(mean_brightness, 3))

    def calculate_glare_ratio(self, image_bgr: np.ndarray) -> float:
        """
        Estimates percentage of saturated specular highlights (reflection/glare).
        Pixels with value > 250 in the brightness channel indicate glare.
        """
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:, :, 2]
        glare_pixels = np.sum(v_channel >= 250)
        total_pixels = v_channel.size
        return float(round(glare_pixels / total_pixels, 3))

    def evaluate_quality(self, image_bgr: np.ndarray) -> Dict[str, Any]:
        """
        Performs comprehensive quality assessment.
        Returns metrics and human-friendly guidance.
        Enforces strict quality gating so low-quality or blank inputs
        are flagged as 'Uncertain / Unable to Verify' instead of falsely classified.
        """
        h, w = image_bgr.shape[:2]
        blur_score = self.calculate_blur(image_bgr)
        brightness = self.calculate_brightness(image_bgr)
        glare_ratio = self.calculate_glare_ratio(image_bgr)

        warnings = []
        is_acceptable = True

        # 1. Blank / Flat image check (std dev of pixels)
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        pixel_std = float(np.std(gray))
        if pixel_std < 10.0 or brightness < 0.06:
            warnings.append("Image appears blank, black, or lacks content.")
            is_acceptable = False

        # 2. Resolution Check
        if h < self.min_resolution[0] or w < self.min_resolution[1]:
            warnings.append(f"Image resolution too low ({w}x{h}). Minimum required is {self.min_resolution[1]}x{self.min_resolution[0]}.")
            is_acceptable = False

        # 3. Blur / Sharpness Check
        if blur_score < 35.0:
            warnings.append(f"Image is severely blurred (sharpness {blur_score:.1f} < 35.0). Hold steady.")
            is_acceptable = False
        elif blur_score < self.min_blur_score:
            warnings.append(f"Image has soft focus (sharpness {blur_score:.1f} < {self.min_blur_score:.1f}).")

        # 4. Brightness Check
        if brightness < self.min_brightness:
            warnings.append(f"Environment is too dark (brightness {brightness:.2f}). Turn on direct room light.")
            is_acceptable = False
        elif brightness > self.max_brightness:
            warnings.append(f"Image is overexposed/washed out (brightness {brightness:.2f}). Reduce direct glare.")
            is_acceptable = False

        # 5. Glare Check
        if glare_ratio > self.max_glare_ratio:
            warnings.append(f"High surface glare detected ({int(glare_ratio*100)}% of surface). Avoid direct reflection.")

        status = "Good" if len(warnings) == 0 else ("Acceptable" if is_acceptable else "Poor")
        
        if not is_acceptable:
            message = "Image quality is insufficient. Keep the entire note inside the frame and improve lighting."
        elif warnings:
            message = " ; ".join(warnings)
        else:
            message = "Image quality is optimal for screening."

        return {
            "is_acceptable": is_acceptable,
            "status": status,
            "blur_score": blur_score,
            "brightness": brightness,
            "glare_ratio": glare_ratio,
            "pixel_std": round(pixel_std, 2),
            "resolution": {"width": w, "height": h},
            "warnings": warnings,
            "message": message
        }

    def locate_held_banknote(self, image_bgr: np.ndarray) -> Tuple[Tuple[int, int, int, int], float, bool]:
        """
        Locates a currency banknote held in front of a camera/webcam scene.
        Uses gradient projections to detect the sharp top/bottom/left/right boundaries
        of the note, separating it from the user's clothing, face, and background.
        """
        h, w = image_bgr.shape[:2]
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        # 1. Edge-based horizontal projection to find top & bottom edges of the note
        sob_y = np.abs(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
        # Focus on middle 70% of X to avoid fingers/edges
        mid_sob_y = sob_y[:, int(w * 0.15):int(w * 0.85)]
        row_grad = np.mean(mid_sob_y, axis=1)

        kernel = np.ones(9) / 9.0
        smooth_grad = np.convolve(row_grad, kernel, mode='same')

        # Search for top edge in range [int(h*0.10) : int(h*0.55)]
        y_min_search = int(h * 0.10)
        y_max_search = int(h * 0.55)
        top_y = y_min_search + int(np.argmax(smooth_grad[y_min_search:y_max_search]))

        # Search for bottom edge in range [top_y + int(h*0.25) : min(h - 20, top_y + int(h*0.65))]
        bot_min = top_y + int(h * 0.25)
        bot_max = min(h - 20, top_y + int(h * 0.65))
        if bot_max > bot_min:
            bot_y = bot_min + int(np.argmax(smooth_grad[bot_min:bot_max]))
        else:
            bot_y = int(h * 0.80)

        note_h = bot_y - top_y
        band_gray = gray[top_y:bot_y, :]
        std_detail = float(np.std(band_gray))

        # 2. Vertical edges in the note horizontal band
        sob_x = np.abs(cv2.Sobel(band_gray, cv2.CV_64F, 1, 0, ksize=3))
        col_grad = np.mean(sob_x, axis=0)
        smooth_col = np.convolve(col_grad, kernel, mode='same')

        # Left edge search [int(w*0.05) : int(w*0.35)]
        left_x = int(w * 0.05) + int(np.argmax(smooth_col[int(w * 0.05):int(w * 0.35)]))
        # Right edge search [int(w*0.65) : int(w*0.95)]
        right_x = int(w * 0.65) + int(np.argmax(smooth_col[int(w * 0.65):int(w * 0.95)]))
        note_w = right_x - left_x

        aspect = float(note_w) / max(1, note_h)

        top_peak_val = float(smooth_grad[top_y])
        bot_peak_val = float(smooth_grad[bot_y])
        mean_grad = float(np.mean(smooth_grad))

        has_strong_edges = (top_peak_val > mean_grad * 1.4) and (bot_peak_val > mean_grad * 1.25)
        is_valid_note = bool((1.40 <= aspect <= 3.10) and (note_h >= h * 0.20) and has_strong_edges and (std_detail >= 25.0))

        return (top_y, bot_y, left_x, right_x), aspect, is_valid_note

    def detect_and_crop_banknote(self, image_bgr: np.ndarray) -> Tuple[np.ndarray, Tuple[int, int, int, int], bool, Dict[str, Any]]:
        """
        Locates the currency note in full camera scenes, crops out background,
        applies perspective correction if the note is slanted/angled, and
        validates whether a recognizable banknote object is present.

        Workflow:
        Input frame -> Contour/Edge Detection -> Polygon Approximation ->
        Perspective Correction (if angled) -> Aspect Ratio Verification ->
        Banknote Candidate Validity Check.
        """
        h, w = image_bgr.shape[:2]
        meta = {
            "is_banknote_detected": True,
            "perspective_corrected": False,
            "aspect_ratio": round(float(w) / max(1, h), 2),
            "detection_method": "full_aspect"
        }

        if w < 100 or h < 60:
            meta["is_banknote_detected"] = False
            return image_bgr, (0, 0, w, h), False, meta

        aspect_input = float(w) / h if h > 0 else 1.0

        # Multi-Device Orientation Normalization:
        # If an already-framed banknote image is oriented vertically (e.g. portrait photo on smartphone),
        # rotate 90 degrees clockwise to align with horizontal currency standards
        if 0.31 <= aspect_input <= 0.74:
            image_bgr = cv2.rotate(image_bgr, cv2.ROTATE_90_CLOCKWISE)
            h, w = image_bgr.shape[:2]
            aspect_input = float(w) / h
            meta["auto_rotated"] = True

        # Standardize ultra-high-resolution smartphone uploads (e.g. 48MP/12MP cameras)
        if max(w, h) > 1920:
            scale = 1600.0 / max(w, h)
            image_bgr = cv2.resize(image_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
            h, w = image_bgr.shape[:2]
            aspect_input = float(w) / h

        # Check for texture / edge variation to reject completely featureless / blank images
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        edge_density = float(np.mean(cv2.Canny(gray, 50, 150)))
        std_dev = float(np.std(gray))

        if edge_density < 1.2 or std_dev < 12.0:
            # Flat wall, blank surface, or unpatterned non-currency
            meta["is_banknote_detected"] = False
            meta["detection_method"] = "insufficient_features"
            return image_bgr, (0, 0, w, h), False, meta

        if (w <= 256 and h <= 256) or (w < 300 and h < 300 and 0.80 <= aspect_input <= 1.25):
            meta["detection_method"] = "pre_scaled_sample"
            return image_bgr, (0, 0, w, h), False, meta

        # Find bounding contour / salient banknote region inside the camera scene
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
        grad = cv2.morphologyEx(blurred, cv2.MORPH_GRADIENT, kernel_rect)
        _, thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_contour = None
        best_box = None
        best_pts = None
        max_score = 0

        for c in contours:
            area = cv2.contourArea(c)
            if area < (h * w * 0.10):  # Must occupy at least 10% of camera field
                continue

            # Approximate polygon
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.03 * peri, True)

            x, y, cw, ch = cv2.boundingRect(c)
            aspect = float(cw) / ch if ch > 0 else 0

            # Centrality score
            cx = x + cw / 2.0
            cy = y + ch / 2.0
            centrality = 1.0 - (abs(cx - w / 2.0) / (w / 2.0) * 0.4 + abs(cy - h / 2.0) / (h / 2.0) * 0.6)
            score = area * max(0.1, centrality)

            if 1.35 <= aspect <= 3.2:
                if score > max_score:
                    max_score = score
                    best_box = (x, y, cw, ch)
                    best_contour = c
                    if len(approx) == 4:
                        best_pts = approx.reshape(4, 2)
            elif 0.31 <= aspect <= 0.74:
                # Vertical banknote held in portrait orientation
                if score > max_score:
                    max_score = score
                    best_box = (x, y, cw, ch)
                    best_contour = c
                    if len(approx) == 4:
                        best_pts = approx.reshape(4, 2)

        # Apply 4-point perspective correction if a clear slanted quadrilateral is detected
        if best_pts is not None and max_score > 0:
            try:
                # Order points: top-left, top-right, bottom-right, bottom-left
                rect = np.zeros((4, 2), dtype="float32")
                s = best_pts.sum(axis=1)
                rect[0] = best_pts[np.argmin(s)]
                rect[2] = best_pts[np.argmax(s)]
                diff = np.diff(best_pts, axis=1)
                rect[1] = best_pts[np.argmin(diff)]
                rect[3] = best_pts[np.argmax(diff)]

                (tl, tr, br, bl) = rect
                wA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                wB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxW = max(int(wA), int(wB))

                hA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                hB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxH = max(int(hA), int(hB))

                if maxW >= 150 and maxH >= 70 and 1.35 <= (float(maxW) / maxH) <= 3.2:
                    dst = np.array([
                        [0, 0],
                        [maxW - 1, 0],
                        [maxW - 1, maxH - 1],
                        [0, maxH - 1]
                    ], dtype="float32")
                    M = cv2.getPerspectiveTransform(rect, dst)
                    warped = cv2.warpPerspective(image_bgr, M, (maxW, maxH))
                    meta["perspective_corrected"] = True
                    meta["detection_method"] = "perspective_warp"
                    meta["aspect_ratio"] = round(float(maxW) / maxH, 2)
                    x, y, cw, ch = cv2.boundingRect(best_contour)
                    return warped, (x, y, cw, ch), True, meta
            except Exception:
                pass

        # Check if the image is already a pre-cropped / framed banknote
        if 1.40 <= aspect_input <= 2.95 and (w <= 850 and h <= 550):
            meta["detection_method"] = "pre_aligned_frame"
            meta["aspect_ratio"] = round(aspect_input, 2)
            meta["is_banknote_detected"] = True
            return image_bgr, (0, 0, w, h), False, meta

        # 1. For full camera scenes: Check for a banknote held in front of the lens
        if w >= 800 and h >= 480:
            held_bbox, held_aspect, is_held_valid = self.locate_held_banknote(image_bgr)
            if is_held_valid:
                ty, by, lx, rx = held_bbox
                cropped = image_bgr[ty:by, lx:rx]
                meta["detection_method"] = "held_banknote_locator"
                meta["aspect_ratio"] = round(held_aspect, 2)
                meta["is_banknote_detected"] = True
                return cropped, (lx, ty, rx - lx, by - ty), True, meta

        # 2. Bounding box fallback (only when contour isolates an actual note cleanly from surroundings)
        if best_box:
            x, y, cw, ch = best_box
            is_entire_frame = (cw >= w * 0.90 and ch >= h * 0.85)
            is_internal_band = (cw >= w * 0.88 and ch < h * 0.70) or (ch >= h * 0.88 and cw < w * 0.70)
            if not is_entire_frame and not is_internal_band and (cw * ch) >= (w * h * 0.20):
                pad_x = int(cw * 0.03)
                pad_y = int(ch * 0.03)
                x0 = max(0, x - pad_x)
                y0 = max(0, y - pad_y)
                x1 = min(w, x + cw + pad_x)
                y1 = min(h, y + ch + pad_y)
                cropped = image_bgr[y0:y1, x0:x1]
                # Validate that the crop has banknote texture (not plain clothing or wall)
                gray_crop = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                sob_x_val = float(np.mean(np.abs(cv2.Sobel(gray_crop, cv2.CV_64F, 1, 0, ksize=3))))
                if sob_x_val >= 14.0:
                    if cropped.shape[0] > cropped.shape[1] * 1.25:
                        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
                    meta["detection_method"] = "bounding_box"
                    meta["aspect_ratio"] = round(float(cropped.shape[1]) / max(1, cropped.shape[0]), 2)
                    meta["is_banknote_detected"] = True
                    return cropped, (x0, y0, x1 - x0, y1 - y0), True, meta

        # 3. Only accept as pre-aligned if image is a compact crop of a note (w <= 800 and h <= 500)
        # Large camera frames (e.g. 1280x720, 1920x1080) without a located note must not pass
        if 1.45 <= aspect_input <= 2.95 and (w <= 800 and h <= 500):
            gray_input = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
            sob_val = float(np.mean(np.abs(cv2.Sobel(gray_input, cv2.CV_64F, 1, 0, ksize=3))))
            if sob_val >= 14.0:
                meta["detection_method"] = "pre_aligned_frame"
                meta["aspect_ratio"] = round(aspect_input, 2)
                meta["is_banknote_detected"] = True
                return image_bgr, (0, 0, w, h), False, meta

        # 4. If it's a large camera scene and no banknote was located in it
        meta["is_banknote_detected"] = False
        meta["detection_method"] = "no_banknote_located"
        return image_bgr, (0, 0, w, h), False, meta

    def enhance_banknote_contrast(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) on the L-channel
        in LAB color space. Normalizes webcam room lighting and reveals micro-printing
        without altering the banknote's authentic color hue.
        """
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl, a, b))
        return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)


# Singleton instance for application-wide use
quality_checker = ImageQualityChecker()

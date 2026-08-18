"""
OpenCV 图像预处理
"""

import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    """读取图片，失败则抛出异常"""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {path}")
    return img


def resize(img: np.ndarray, max_side: int = 1280) -> np.ndarray:
    """等比缩放，长边不超过 max_side"""
    h, w = img.shape[:2]
    if max(h, w) <= max_side:
        return img
    scale = max_side / max(h, w)
    return cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)


def to_gray(img: np.ndarray) -> np.ndarray:
    """转灰度图"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def to_binary(img: np.ndarray) -> np.ndarray:
    """Otsu 自动阈值二值化"""
    gray = to_gray(img) if len(img.shape) == 3 else img
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def enlarge(img: np.ndarray, factor: float = 2.0) -> np.ndarray:
    """放大图片"""
    h, w = img.shape[:2]
    return cv2.resize(img, (int(w * factor), int(h * factor)), interpolation=cv2.INTER_CUBIC)


def draw_boxes(img: np.ndarray, items: list) -> np.ndarray:
    """在图片上绘制识别框和文字，返回绘制后的副本"""
    vis = img.copy()
    for it in items:
        pts = np.array([[int(p[0]), int(p[1])] for p in it["box"]], dtype=np.int32)
        cv2.polylines(vis, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(vis, it["text"], (pts[0][0], pts[0][1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return vis

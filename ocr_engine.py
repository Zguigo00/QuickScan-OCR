"""
OCR 模型初始化与识别
"""

import cv2
from paddleocr import PaddleOCR


def create_ocr_engine():
    """初始化 PaddleOCR 引擎"""
    return PaddleOCR(use_angle_cls=True, lang="ch")


def recognize(ocr_engine, img):
    """
    对图片运行 OCR 识别
    返回: list[dict] — 每条包含 text, confidence, box, x, y, width, height
    """
    results = ocr_engine.ocr(img, cls=True)
    items = []
    for line in results:
        if line is None:
            continue
        for box, (text, confidence) in line:
            x_min = min(p[0] for p in box)
            y_min = min(p[1] for p in box)
            x_max = max(p[0] for p in box)
            y_max = max(p[1] for p in box)
            items.append({
                "text": text,
                "confidence": round(confidence, 4),
                "box": box,
                "x": round(x_min, 1),
                "y": round(y_min, 1),
                "width": round(x_max - x_min, 1),
                "height": round(y_max - y_min, 1),
            })
    return items

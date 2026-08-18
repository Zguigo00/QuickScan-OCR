"""
OCR 项目主入口
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from ocr_engine import create_ocr_engine, recognize
from preprocess import load_image, resize, draw_boxes
from parser import sort_reading_order, extract_fields
from output import save_json, save_image, print_results

IMG_PATH = "images/exec.png"
JSON_PATH = "results/result.json"
RESULT_IMG_PATH = "results/ocr_result.jpg"


def main():
    # ① OCR 识别
    print("① OCR 识别中...")
    ocr = create_ocr_engine()
    img = load_image(IMG_PATH)
    img = resize(img)
    items = recognize(ocr, img)
    print(f"   识别到 {len(items)} 条文字")

    # ② 按阅读顺序排序
    print("② 按阅读顺序排序...")
    items = sort_reading_order(items)

    # ③ 提取关键字段
    print("③ 提取关键字段...")
    fields = extract_fields(items)

    # ④ 保存 JSON
    print("④ 保存 JSON...")
    save_json(items, fields, JSON_PATH)

    # ⑤ 绘制标注图
    print("⑤ 绘制标注图...")
    vis = draw_boxes(img, items)
    save_image(vis, RESULT_IMG_PATH)

    # ⑥ 打印结果
    print_results(items, fields)


if __name__ == "__main__":
    main()

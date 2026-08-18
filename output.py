"""
JSON 输出与结果保存
"""

import json
import cv2
import numpy as np


def save_json(items: list, fields: dict, output_path: str):
    """保存识别结果和关键字段到 JSON"""
    result = {
        "total_items": len(items),
        "items": items,
        "fields": fields,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"JSON 已保存到: {output_path}")


def save_image(img: np.ndarray, output_path: str):
    """保存图片"""
    cv2.imwrite(output_path, img)
    print(f"图片已保存到: {output_path}")


def print_results(items: list, fields: dict):
    """打印识别结果到终端"""
    print("\n" + "=" * 50)
    print("全部识别文本（阅读顺序）:")
    print("=" * 50)
    for i, it in enumerate(items, 1):
        print(f"  {i}. [{it['confidence']:.2f}] {it['text']}")

    if fields:
        print("\n" + "=" * 50)
        print("提取到的关键字段:")
        print("=" * 50)
        for k, v in fields.items():
            print(f"  {k}: {', '.join(v)}")
    else:
        print("\n未提取到金额/日期/编号")

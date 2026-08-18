"""
信息提取：从 OCR 结果中按阅读顺序排序，提取金额/日期/编号
"""

import re


def sort_reading_order(items: list, line_threshold: int = 20) -> list:
    """
    按阅读顺序排序：
    - 先按 y 坐标分行（y 差值 < line_threshold 视为同一行）
    - 同一行内按 x 坐标从左到右
    """
    if not items:
        return items

    sorted_items = sorted(items, key=lambda it: it["y"])
    lines = []
    current_line = [sorted_items[0]]

    for item in sorted_items[1:]:
        if abs(item["y"] - current_line[0]["y"]) < line_threshold:
            current_line.append(item)
        else:
            lines.append(current_line)
            current_line = [item]
    lines.append(current_line)

    result = []
    for line in lines:
        line.sort(key=lambda it: it["x"])
        result.extend(line)
    return result


def extract_fields(items: list) -> dict:
    """
    从识别文本中自动提取金额、日期、编号
    返回: {"金额": [...], "日期": [...], "编号": [...]} — 仅包含有值的字段
    """
    full_text = " ".join(it["text"] for it in items)

    fields = {
        "金额": [],
        "日期": [],
        "编号": [],
    }

    # 金额
    for pattern in [
        r"[¥￥]\s*(\d+[\.,]?\d*)",
        r"(\d+[\.,]?\d*)\s*元",
        r"金额[：:]\s*(\d+[\.,]?\d*)",
        r"合计[：:]\s*(\d+[\.,]?\d*)",
        r"总价[：:]\s*(\d+[\.,]?\d*)",
        r"(\d+[\.,]?\d*)\s*圆",
    ]:
        for m in re.finditer(pattern, full_text):
            val = m.group(1)
            if val not in fields["金额"]:
                fields["金额"].append(val)

    # 日期
    for pattern in [
        r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)",
        r"(\d{2}[-/]\d{1,2}[-/]\d{1,2})",
        r"日期[：:]\s*(.+?)(?:\s|$)",
    ]:
        for m in re.finditer(pattern, full_text):
            val = m.group(1)
            if val not in fields["日期"]:
                fields["日期"].append(val)

    # 编号
    for pattern in [
        r"[编号单]\s*[号码编]\s*[：:]\s*([A-Za-z0-9\-]+)",
        r"订单[号编]\s*[：:]\s*([A-Za-z0-9\-]+)",
        r"发票[号码]\s*[：:]\s*([A-Za-z0-9\-]+)",
        r"No[.:]\s*([A-Za-z0-9\-]+)",
        r"编号[：:]\s*([A-Za-z0-9\-]+)",
    ]:
        for m in re.finditer(pattern, full_text, re.IGNORECASE):
            val = m.group(1)
            if val not in fields["编号"]:
                fields["编号"].append(val)

    return {k: v for k, v in fields.items() if v}

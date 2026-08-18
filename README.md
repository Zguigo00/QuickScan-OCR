# QuickScan-OCR

基于 PaddleOCR 的图片文字识别工具，支持中文识别、按阅读顺序排序、自动提取金额/日期/编号等关键字段。

## 项目结构

```
QuickScan-OCR/
├── main.py          # 程序主入口
├── ocr_engine.py    # OCR 模型初始化与识别
├── preprocess.py    # OpenCV 图像预处理（缩放、灰度、二值化等）
├── parser.py        # 阅读顺序排序 + 关键字段提取
├── output.py        # JSON 输出与结果保存
│
├── images/          # 测试图片
└── results/         # 输出结果（result.json + 标注图）
```

## 环境依赖

- Python 3.11+
- PaddlePaddle 2.6.2
- PaddleOCR 2.8.1
- OpenCV

## 安装

```bash
# 创建虚拟环境
python -m venv .venv
.\.venv\Scripts\activate

# 安装依赖
pip install paddlepaddle==2.6.2 paddleocr==2.8.1 opencv-python
```

## 使用

将待识别的图片放入 `images/` 文件夹，修改 `main.py` 中的 `IMG_PATH`，然后运行：

```bash
python main.py
```

输出结果保存在 `results/` 文件夹：
- `result.json` — 结构化识别结果（文字、坐标、置信度、关键字段）
- `ocr_result.jpg` — 标注了识别框的图片

## 识别流程

```
图片输入
  ↓
OpenCV 预处理（缩放）
  ↓
PaddleOCR 识别
  ↓
提取文字 / 坐标 / 置信度
  ↓
按阅读顺序排序（从上到下，同行从左到右）
  ↓
自动提取关键字段（金额 / 日期 / 编号）
  ↓
输出 JSON + 标注图
```

## JSON 输出示例

```json
{
  "total_items": 8,
  "items": [
    {
      "text": "MDX格式文章示例",
      "confidence": 0.9965,
      "box": [[29.0, 33.0], [206.0, 33.0], [206.0, 55.0], [29.0, 55.0]],
      "x": 29.0,
      "y": 33.0,
      "width": 177.0,
      "height": 22.0
    }
  ],
  "fields": {
    "日期": ["1970-01-02"]
  }
}
```

## License

MIT

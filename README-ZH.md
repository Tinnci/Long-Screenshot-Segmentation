# 网页长截图分割工具

[![PyPI - Version](https://img.shields.io/pypi/v/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Tinnci/Long-Screenshot-Segmentation/python-publish.yml)](https://github.com/Tinnci/Long-Screenshot-Segmentation/actions/workflows/python-publish.yml)
[![PyPI - License](https://img.shields.io/pypi/l/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![Static Badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-8A2BE2)](README-ZH.md)
[![Static Badge](https://img.shields.io/badge/English-blue)](README.md)

## 项目介绍

本项目用于将网页的长截图自动分割成多个完整的小图像。通过检测图像中的**空白区域**和**颜色变化**来识别分割点，适合用于：

- 使用 [screenshot-to-code](https://github.com/abi/screenshot-to-code) 等工具生成网页代码
- 为机器学习模型准备训练数据
- 将长网页截图分割成可管理的块

![红线为分割线](images/demo.png)

**更多示例见** [images](images) 目录

## 分割原理

### 1. 空白区域检测
计算图像每一行像素的**拉普拉斯方差**，低方差表示该行像素变化少（空白区域），作为潜在分割点。

### 2. 颜色变化检测
计算相邻行之间的**颜色差异**，大的颜色差异表示视觉分离，作为潜在分割点。

### 3. 合并分割点
过滤距离过近的分割点，避免过度分割，确保每个分割区域都有意义。

## 安装

### 使用 pip
```bash
pip install long-screenshot-segmentation
```

### 使用 uv（推荐）
```bash
uv tool install long-screenshot-segmentation
```

### 从源码安装
```bash
git clone https://github.com/Tinnci/Long-Screenshot-Segmentation.git
cd Long-Screenshot-Segmentation
uv venv
.venv\Scripts\activate  # Windows
# 或 source .venv/bin/activate  # Linux/macOS
uv pip install -e .
```

## 命令行使用

### screenshot-segment（获取分割点）

```bash
# 获取分割线高度
screenshot-segment -f "C:\path\to\image.png"
# 输出: [818, 1680, 2264, 2745, 4036, 5407, 6210, 6678, 7345, 7856, 8543, 9245, 10504, 11512]

# 保存带有分割线的图像
screenshot-segment -f "C:\path\to\image.png" -s True

# 导出分割区域为单独的图像
screenshot-segment -f "C:\path\to\image.png" -e True

# 导出分割区域并自动裁剪空白边缘
screenshot-segment -f "C:\path\to\image.png" -e True -crop True

# 自定义阈值
screenshot-segment -f "C:\path\to\image.png" \
  -ht 150 \
  -vt 0.3 \
  -ct 120 \
  -mt 400
```

**参数说明：**
- `-f, --file`: 图像文件路径（必需）
- `-s, --split`: 是否保存带分割线的图像（默认: False）
- `-o, --output_dir`: 输出目录（默认: result）
- `-ht, --height_threshold`: 空白区域高度阈值（默认: 102）
- `-vt, --variation_threshold`: 变化阈值（默认: 0.5）
- `-ct, --color_threshold`: 颜色差异阈值（默认: 100）
- `-cvt, --color_variation_threshold`: 颜色差异变化阈值（默认: 15）
- `-mt, --merge_threshold`: 分割点合并距离（默认: 350）
- `-e, --export`: 是否导出分割区域为单独图像（默认: False）
- `-seg, --segments_dir`: 分割图像保存目录（默认: segments）
- `-crop, --auto_crop`: 是否自动裁剪空白边缘（默认: False）
- `-crop_t, --crop_threshold`: 空白区域检测阈值 (0-255，默认: 240)
- `-crop_h, --crop_min_width`: 裁剪后保留的最小宽度（默认: 50）

### screenshot-draw（绘制分割线）

```bash
screenshot-draw --image_file path/to/image.jpg --heights 100 200 300 --color 0,255,0
```

### screenshot-split（切分图像）

```bash
screenshot-split --image_file path/to/image.jpg --heights 233 456 789
```

## Python API 使用

### 方法 1: split_heights（推荐）

```python
from Web_page_Screenshot_Segmentation.master import split_heights

# 获取分割点
heights = split_heights("my_screenshot.png")
print(heights)  # [100, 200, 300, ...]

# 保存带分割线的图像
result_path = split_heights(
    "my_screenshot.png",
    split=True,
    output_dir="result",
    height_threshold=102,
    variation_threshold=0.5,
    color_threshold=100,
    color_variation_threshold=15,
    merge_threshold=350
)
print(f"图像已保存到: {result_path}")
```

### 方法 2: split_and_export_segments（导出分割区域）

```python
from Web_page_Screenshot_Segmentation.master import split_and_export_segments

# 导出所有分割区域为单独的图像
output_dir = split_and_export_segments(
    "my_screenshot.png",
    output_dir="segments"
)
print(f"分割区域已保存到: {output_dir}")

# 导出分割区域并自动裁剪空白边缘
output_dir = split_and_export_segments(
    "my_screenshot.png",
    output_dir="segments_cropped",
    auto_crop=True,
    crop_threshold=240,
    crop_min_width=50
)
print(f"裁剪后的分割区域已保存到: {output_dir}")
```

**参数说明：**
- `file_path`: 图像文件路径
- `output_dir`: 分割图像保存目录（默认: segments）
- `auto_crop`: 是否移除空白边缘（默认: False）
- `crop_threshold`: 空白区域检测阈值 (0-255，默认: 240)
- `crop_min_width`: 裁剪后保留的最小宽度（默认: 50）
- `height_threshold`, `variation_threshold`, `color_threshold`, `color_variation_threshold`, `merge_threshold`: 同 `split_heights` 中的参数

**自动裁剪算法：**
自动裁剪功能通过分析以下特征来智能检测内容：
1. **像素方差** — 文本和图形具有像素值变化
2. **深色像素** — 内容通常比白色背景暗

任何具有显著方差或深色像素的列都会被保留。只有真正的空白列才会被删除。

### 方法 2: draw_line_from_file（绘制分割线）

```python
from Web_page_Screenshot_Segmentation.drawer import draw_line_from_file

result_path = draw_line_from_file(
    image_file="my_screenshot.png",
    heights=[100, 200, 300],
    color=(0, 255, 0)  # BGR 格式: 绿色
)
print(f"图像已保存到: {result_path}")
```

### 方法 3: split_and_save_image（分割图像）

```python
import cv2
from Web_page_Screenshot_Segmentation.spliter import split_and_save_image

image = cv2.imread("my_screenshot.png")
result_dir = split_and_save_image(
    image,
    heights=[868, 1912, 2672],
    output_dir="split_images"
)
print(f"分割图像已保存到: {result_dir}")
```

## 特性

✅ **双重检测方法** — 结合空白区域检测和颜色变化检测，提高分割准确性  
✅ **Unicode 文件名支持** — 支持中文、日文等非 ASCII 字符的文件名  
✅ **分割导出功能** — 将分割后的区域保存为独立图像  
✅ **智能自动裁剪** — 移除空白边缘，同时保留所有文本和内容  
✅ **灵活的阈值参数** — 可根据不同图像类型调整检测灵敏度  
✅ **多种输出格式** — 获取分割点、绘制分割线或导出分割图像  
✅ **跨平台兼容** — Windows、Linux、macOS 完全支持  

## 测试

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行所有测试
pytest -v

# 生成覆盖率报告
pytest --cov=Web_page_Screenshot_Segmentation --cov-report=html
```

详见 [README_TESTING.md](README_TESTING.md)

## 贡献

欢迎提交 Issue 或 Pull Request！

## 致谢

本项目基于 [Tim-Saijun](https://github.com/Tim-Saijun) 的原始项目进行优化和改进。

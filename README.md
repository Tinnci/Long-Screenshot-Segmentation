# Long Screenshot Segmentation

[![PyPI - Version](https://img.shields.io/pypi/v/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ryaang/Web-page-Screenshot-Segmentation/python-publish.yml)](https://github.com/Ryaang/Web-page-Screenshot-Segmentation/actions/workflows/python-publish.yml)
[![PyPI - License](https://img.shields.io/pypi/l/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![Static Badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-8A2BE2)](README-ZH.md)
[![Static Badge](https://img.shields.io/badge/English-blue)](README.md)

This project provides a tool to segment long web page screenshots into smaller, more manageable images. This is particularly useful for tasks like training machine learning models on web page data or for use with tools like [screenshot-to-code](https://github.com/abi/screenshot-to-code).

![The Red lines are split lines](images/demo.png)

## Methodology

The segmentation process is based on two main computer vision techniques:

### 1. Blank Space Detection

This method identifies horizontal blank spaces in the screenshot. It works by calculating the **Laplacian variance** for each row of pixels in the image. A low variance indicates a region with little change, which is likely a blank space. The algorithm identifies these low-variance regions and marks their vertical midpoints as potential split points.

### 2. Color-Based Detection

This method detects sharp changes in color between adjacent rows of pixels. It calculates the average color for each row and then computes the color difference between consecutive rows. A large color difference suggests a visual separation and is marked as a potential split point.

### 3. Merging Split Points

After identifying all potential split points from both methods, the algorithm merges any points that are too close to each other. This is done to avoid over-segmentation and to ensure that the resulting images are meaningful and not too small.

## Installation

You can install the package from PyPI:

```bash
pip install Web-page-Screenshot-Segmentation
```

## Usage

### Command-Line Interface

This package provides three command-line tools for easy use:

#### `screenshot-segment`

This is the main tool for finding the split points in an image.

```bash
screenshot-segment <image_file> [--split] [--output_dir <dir>]
```

-   `<image_file>`: Path to the image file.
-   `--split`: If provided, the tool will save the image with the split lines drawn on it.
-   `--output_dir`: The directory to save the output image (default: `result`).

**Example:**

```bash
# Get the split points for an image
screenshot-segment my_screenshot.png

# Save the image with the split lines drawn
screenshot-segment my_screenshot.png --split
```

#### `screenshot-draw`

This tool allows you to draw lines on an image at specified heights.

```bash
screenshot-draw <image_file> --heights <h1, h2, ...> [--color <b,g,r>] [--output_dir <dir>]
```

-   `<image_file>`: Path to the image file.
-   `--heights`: A list of heights to draw lines at.
-   `--color`: The color of the lines in B,G,R format (e.g., '0,0,255' for red).
-   `--output_dir`: The directory to save the output image (default: `result`).

**Example:**

```bash
screenshot-draw my_screenshot.png --heights 100 200 300
```

#### `screenshot-split`

This tool splits an image into multiple parts based on a list of heights.

```bash
screenshot-split <image_file> --heights <h1, h2, ...> [--output_dir <dir>]
```

-   `<image_file>`: Path to the image file.
-   `--heights`: A list of heights to split the image at.
-   `--output_dir`: The directory to save the split images (default: `split_images`).

**Example:**

```bash
screenshot-split my_screenshot.png --heights 868 1912 2672
```

### Python API

You can also use the library directly in your Python code:

#### `split_heights`

The `split_heights` function is the main function for finding the split points.

```python
from Web_page_Screenshot_Segmentation.master import split_heights

# Get the split points for an image
heights = split_heights("my_screenshot.png")
print(heights)

# Save the image with the split lines drawn
result_path = split_heights("my_screenshot.png", split=True)
print(f"Image saved to: {result_path}")
```

#### `draw_line_from_file`

The `draw_line_from_file` function allows you to draw lines on an image.

```python
from Web_page_Screenshot_Segmentation.drawer import draw_line_from_file

result_path = draw_line_from_file("my_screenshot.png", heights=[100, 200, 300])
print(f"Image saved to: {result_path}")
```

#### `split_and_save_image`

The `split_and_save_image` function splits an image into multiple parts.

```python
import cv2
from Web_page_Screenshot_Segmentation.spliter import split_and_save_image

image = cv2.imread("my_screenshot.png")
result_path = split_and_save_image(image, heights=[868, 1912, 2672], output_dir="my_split_images")
print(f"Images saved to: {result_path}")
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

To set up the development environment:

1.  Clone the repository.
2.  Create a virtual environment and activate it.
3.  Install the dependencies: `pip install -e .[dev]`

## Acknowledgments

This project is a fork of the [Long-Screenshot-Segmentation](https://github.com/Tim-Saijun/Long-Screenshot-Segmentation) repository by [Tim-Saijun](https://github.com/Tim-Saijun). We are grateful for their original work.
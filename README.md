# Long Screenshot Segmentation

[![PyPI - Version](https://img.shields.io/pypi/v/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Tinnci/Long-Screenshot-Segmentation/python-publish.yml)](https://github.com/Tinnci/Long-Screenshot-Segmentation/actions/workflows/python-publish.yml)
[![PyPI - License](https://img.shields.io/pypi/l/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)
[![Static Badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-8A2BE2)](README-ZH.md)
[![Static Badge](https://img.shields.io/badge/English-blue)](README.md)

## Features

- **Dual Detection Methods** — Combines blank space detection and color-based splitting for accurate segmentation
- **Unicode File Support** — Handles filenames with Chinese characters and other non-ASCII characters
- **Export Segments** — Save individual segmented areas as standalone images
- **Auto-Crop** — Intelligently removes blank/white margins while preserving all text and content
- **Flexible Thresholds** — Customize detection sensitivity for different image types
- **Multiple Output Formats** — Get split points, draw lines, or export segments
- **Cross-Platform** — Works on Windows, Linux, and macOS

## Methodology

The segmentation process is based on two main computer vision techniques:

### 1. Blank Space Detection

This method identifies horizontal blank spaces in the screenshot. It works by calculating the **Laplacian variance** for each row of pixels in the image. A low variance indicates a region with little change, which is likely a blank space. The algorithm identifies these low-variance regions and marks their vertical midpoints as potential split points.

### 2. Color-Based Detection

This method detects sharp changes in color between adjacent rows of pixels. It calculates the average color for each row and then computes the color difference between consecutive rows. A large color difference suggests a visual separation and is marked as a potential split point.

### 3. Merging Split Points

After identifying all potential split points from both methods, the algorithm merges any points that are too close to each other. This is done to avoid over-segmentation and to ensure that the resulting images are meaningful and not too small.

## Installation

To install the package from this repository, navigate to the project's root directory and run:

```bash
pip install .
```

Alternatively, for a more isolated and efficient installation of the command-line tools, you can use `uv tool install` from the project's root directory:

```bash
uv tool install .
```

## Usage

### Command-Line Interface

This package provides three command-line tools for easy use:

#### `screenshot-segment`

This is the main tool for finding the split points in an image.

```bash
screenshot-segment <image_file> [OPTIONS]
```

**Options:**
- `-f, --file`: Path to the image file (required)
- `-s, --split`: Save image with split lines drawn (default: False)
- `-o, --output_dir`: Output directory for split image (default: `result`)
- `-ht, --height_threshold`: Blank area height threshold (default: 102)
- `-vt, --variation_threshold`: Variation threshold (default: 0.5)
- `-ct, --color_threshold`: Color difference threshold (default: 100)
- `-cvt, --color_variation_threshold`: Color variation threshold (default: 15)
- `-mt, --merge_threshold`: Minimum distance between split lines (default: 350)
- `-e, --export`: Export segments as separate images (default: False)
- `-seg, --segments_dir`: Directory to save segment images (default: `segments`)
- `-crop, --auto_crop`: Auto-crop blank areas from segment edges (default: False)
- `-crop_t, --crop_threshold`: Threshold for detecting blank areas (default: 240)
- `-crop_h, --crop_min_width`: Minimum width to preserve after cropping (default: 50)

**Examples:**

```bash
# Get the split points for an image
screenshot-segment my_screenshot.png

# Save the image with the split lines drawn
screenshot-segment my_screenshot.png -s True

# Export segments as separate images
screenshot-segment my_screenshot.png -e True

# Export segments with auto-crop to remove blank margins
screenshot-segment my_screenshot.png -e True -crop True

# Custom parameters
screenshot-segment my_screenshot.png \
  -ht 150 \
  -vt 0.3 \
  -ct 120 \
  -mt 400 \
  -e True \
  -crop True \
  -crop_t 230
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

### `split_and_export_segments`

Export segmented areas as separate standalone images, with optional auto-crop.

```python
from Web_page_Screenshot_Segmentation.master import split_and_export_segments

# Export all segments without cropping
output_dir = split_and_export_segments(
    "my_screenshot.png",
    output_dir="segments"
)
print(f"Segments saved to: {output_dir}")

# Export with auto-crop to remove blank margins
output_dir = split_and_export_segments(
    "my_screenshot.png",
    output_dir="segments_cropped",
    auto_crop=True,
    crop_threshold=240,
    crop_min_width=50
)
print(f"Cropped segments saved to: {output_dir}")
```

**Parameters:**
- `file_path`: Path to the image file
- `output_dir`: Directory to save segments (default: `segments`)
- `auto_crop`: Whether to remove blank areas (default: False)
- `crop_threshold`: Pixel threshold for blank detection (0-255, default: 240)
- `crop_min_width`: Minimum width to preserve (default: 50)
- `height_threshold`, `variation_threshold`, `color_threshold`, `color_variation_threshold`, `merge_threshold`: Same as `split_heights`

**Auto-Crop Algorithm:**
The auto-crop feature intelligently detects content by analyzing:
1. **Pixel Variance** — Text and graphics have varying pixel values
2. **Dark Pixels** — Content is typically darker than the white background

Any column with significant variance or dark pixels is preserved. Only truly blank columns are removed.

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
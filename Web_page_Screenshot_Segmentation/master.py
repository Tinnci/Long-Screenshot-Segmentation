import cv2
import os
import argparse
import numpy as np
from .blank_spliter import find_height_spliter
from .color_spliter import color_height_spliter
from .drawer import draw_line


def remove_close_values(
    lst: list[int], threshold: int, min_height: int = 200
) -> list[int]:
    """
    Removes values from a list that are too close to each other.

    Given a list of integers, this function sorts the list and removes values
    that have a difference less than or equal to the given threshold. It
    also removes any values less than `min_height`.

    :param lst: A list of integers.
    :param threshold: The minimum difference between two values to keep them.
    :param min_height: The minimum height to keep a value.
    :return: A new list with the filtered values.
    """
    if not lst:
        return []

    # Filter out values less than min_height
    lst = [val for val in lst if val >= min_height]
    if not lst:
        return []

    lst.sort()

    # Build a new list with the filtered values
    result = [lst[0]]
    for i in range(1, len(lst)):
        if lst[i] - result[-1] > threshold:
            result.append(lst[i])

    return result


def auto_crop_image(
    image: np.ndarray, threshold: int = 240, min_height: int = 50
) -> np.ndarray:
    """
    Automatically crops blank/white areas from image edges.

    This function removes mostly blank (white or near-white) rows from the top
    and bottom of an image. Useful for removing empty space from segmented areas.

    :param image: The input image as a NumPy array (BGR format).
    :param threshold: Pixel value threshold for detecting blank rows (0-255).
                      Rows where all pixels are above this value are considered blank.
    :param min_height: Minimum height to keep (prevents over-cropping).
    :return: The cropped image.
    """
    if image.shape[0] <= min_height:
        return image

    # Convert to grayscale for analysis
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Find rows where most pixels are "blank" (high values)
    row_means = gray.mean(axis=1)
    blank_rows = row_means > threshold

    # Find first and last non-blank rows
    non_blank_indices = np.where(~blank_rows)[0]

    if len(non_blank_indices) == 0:
        # All blank, return original
        return image

    top = non_blank_indices[0]
    bottom = non_blank_indices[-1] + 1

    # Ensure minimum height
    if bottom - top < min_height:
        return image

    return image[top:bottom, :]


def split_heights(
    file_path: str,
    split: bool = False,
    output_dir: str = "result",
    height_threshold: int = 102,
    variation_threshold: float = 0.5,
    color_threshold: int = 100,
    color_variation_threshold: int = 15,
    merge_threshold: int = 350,
) -> list[int] | str:
    """
    Splits a long web page screenshot into several parts based on visual cues.

    This function analyzes an image to find horizontal split points based on
    low variation regions (blank spaces) and color differences. It can return
    the heights of the split lines or save the split image with the lines drawn.

    :param file_path: Path to the image file.
    :param split: If True, saves the image with split lines drawn.
    :param output_dir: The directory to save the split image.
    :param height_threshold: The height threshold for low variation regions.
    :param variation_threshold: The variation threshold for low variation regions.
    :param color_threshold: The threshold for color differences.
    :param color_variation_threshold: The threshold for color difference variations.
    :param merge_threshold: The minimum distance between two split lines.
    :return: A list of split line heights or the path to the split image.
    """
    print(f"Debug: file_path received: {file_path}")
    try:
        # Read image as a byte stream to handle non-ASCII file paths
        img_data = np.fromfile(file_path, np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(
                f"Image not found or could not be decoded at path: {file_path}"
            )
    except Exception as e:
        raise IOError(f"Failed to read image file: {e}")

    heights = []
    regions = find_height_spliter(img, height_threshold, variation_threshold)
    heights.extend(regions)
    regions = color_height_spliter(img, color_threshold, color_variation_threshold)
    heights.extend(regions)
    heights = remove_close_values(heights, merge_threshold)

    if split:
        os.makedirs(output_dir, exist_ok=True)
        draw_line(img, heights, color=(0, 255, 0))

        base_name, ext = os.path.splitext(os.path.basename(file_path))
        output_filename = f"{base_name}_result.jpg"
        output_path = os.path.join(output_dir, output_filename)

        # Use imencode + binary write to handle Unicode filenames
        success, encoded_img = cv2.imencode(".jpg", img)
        if success:
            with open(output_path, "wb") as f:
                f.write(encoded_img)
        else:
            raise IOError(f"Failed to encode image for writing to {output_path}")

        return os.path.abspath(output_path)
    else:
        return heights


def split_and_export_segments(
    file_path: str,
    output_dir: str = "segments",
    height_threshold: int = 102,
    variation_threshold: float = 0.5,
    color_threshold: int = 100,
    color_variation_threshold: int = 15,
    merge_threshold: int = 350,
    auto_crop: bool = False,
    crop_threshold: int = 240,
    crop_min_height: int = 50,
) -> str:
    """
    Detects split points and exports each segmented area as a standalone image.

    This function analyzes an image to find horizontal split points, then saves
    each segmented area as an individual image file in the output directory.
    Optionally applies auto-cropping to remove blank areas from segments.

    :param file_path: Path to the image file.
    :param output_dir: The directory to save the segmented images (default: 'segments').
    :param height_threshold: The height threshold for low variation regions.
    :param variation_threshold: The variation threshold for low variation regions.
    :param color_threshold: The threshold for color differences.
    :param color_variation_threshold: The threshold for color difference variations.
    :param merge_threshold: The minimum distance between two split lines.
    :param auto_crop: Whether to auto-crop blank areas from segments (default: False).
    :param crop_threshold: Pixel threshold for detecting blank areas (0-255, default: 240).
    :param crop_min_height: Minimum height to preserve after cropping (default: 50).
    :return: The absolute path to the output directory containing all segments.
    """
    # Get split heights
    heights = split_heights(
        file_path,
        split=False,
        height_threshold=height_threshold,
        variation_threshold=variation_threshold,
        color_threshold=color_threshold,
        color_variation_threshold=color_variation_threshold,
        merge_threshold=merge_threshold,
    )

    # Read the image
    try:
        img_data = np.fromfile(file_path, np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(
                f"Image not found or could not be decoded at path: {file_path}"
            )
    except Exception as e:
        raise IOError(f"Failed to read image file: {e}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get original filename without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Split and save segments
    img_height = img.shape[0]
    split_heights_list = sorted(list(set([0] + heights + [img_height])))

    segment_count = 0
    cropped_count = 0
    for i in range(len(split_heights_list) - 1):
        start_y = split_heights_list[i]
        end_y = split_heights_list[i + 1]

        # Extract segment
        segment = img[start_y:end_y, :]

        # Apply auto-crop if enabled
        if auto_crop:
            cropped_segment = auto_crop_image(
                segment, threshold=crop_threshold, min_height=crop_min_height
            )
            if cropped_segment.shape[0] != segment.shape[0]:
                segment = cropped_segment
                cropped_count += 1

        # Save segment with descriptive name
        segment_filename = f"{base_name}_segment_{segment_count:03d}.jpg"
        segment_path = os.path.join(output_dir, segment_filename)

        # Use imencode + binary write for Unicode filename support
        success, encoded_img = cv2.imencode(".jpg", segment)
        if success:
            with open(segment_path, "wb") as f:
                f.write(encoded_img)
            segment_count += 1
        else:
            raise IOError(f"Failed to encode image for writing to {segment_path}")

    message = f"✓ Exported {segment_count} segments to: {os.path.abspath(output_dir)}"
    if auto_crop:
        message += f" (auto-cropped {cropped_count} segments)"
    print(message)
    return os.path.abspath(output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="path of the image file")
    parser.add_argument(
        "-s", "--split", type=bool, default=False, help="whether to split the image"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="result",
        help="the directory to save the split image",
    )
    parser.add_argument(
        "-ht",
        "--height_threshold",
        type=int,
        default=102,
        help="the height threshold of the low variation region",
    )
    parser.add_argument(
        "-vt",
        "--variation_threshold",
        type=float,
        default=0.5,
        help="the variation threshold of the low variation region",
    )
    parser.add_argument(
        "-ct",
        "--color_threshold",
        type=int,
        default=100,
        help="the threshold of the color difference",
    )
    parser.add_argument(
        "-cvt",
        "--color_variation_threshold",
        type=int,
        default=15,
        help="the threshold of the color difference variation",
    )
    parser.add_argument(
        "-mt",
        "--merge_threshold",
        type=int,
        default=350,
        help="the threshold of the least distance between two lines",
    )
    parser.add_argument(
        "-e",
        "--export",
        type=bool,
        default=False,
        help="whether to export segmented areas as separate images",
    )
    parser.add_argument(
        "-seg",
        "--segments_dir",
        type=str,
        default="segments",
        help="the directory to save segmented images (used with --export)",
    )
    parser.add_argument(
        "-crop",
        "--auto_crop",
        type=bool,
        default=False,
        help="whether to auto-crop blank areas from segments (only with --export)",
    )
    parser.add_argument(
        "-crop_t",
        "--crop_threshold",
        type=int,
        default=240,
        help="pixel threshold for detecting blank areas (0-255, higher=more aggressive)",
    )
    parser.add_argument(
        "-crop_h",
        "--crop_min_height",
        type=int,
        default=50,
        help="minimum height to preserve after cropping",
    )
    args = parser.parse_args()

    if args.export:
        # Export segments with optional auto-crop
        res = split_and_export_segments(
            args.file,
            args.segments_dir,
            args.height_threshold,
            args.variation_threshold,
            args.color_threshold,
            args.color_variation_threshold,
            args.merge_threshold,
            args.auto_crop,
            args.crop_threshold,
            args.crop_min_height,
        )
    else:
        # Original behavior: get split heights or split image
        res = split_heights(
            args.file,
            args.split,
            args.output_dir,
            args.height_threshold,
            args.variation_threshold,
            args.color_threshold,
            args.color_variation_threshold,
            args.merge_threshold,
        )
    print(res)


if __name__ == "__main__":
    main()

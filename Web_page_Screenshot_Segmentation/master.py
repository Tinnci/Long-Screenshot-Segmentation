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
    args = parser.parse_args()
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

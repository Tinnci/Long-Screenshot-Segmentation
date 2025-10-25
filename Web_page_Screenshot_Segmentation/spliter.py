import cv2
import argparse
import os
from pathlib import Path
from PIL import Image
from io import BytesIO
import numpy as np


def split_and_save_image(image: np.ndarray, heights: list[int], output_dir: str) -> str:
    """
    Splits an image into multiple parts based on a list of heights and saves them.

    :param image: The input image as a NumPy array.
    :param heights: A list of integer heights to split the image at.
    :param output_dir: The directory to save the split images.
    :return: The absolute path to the output directory.
    """
    img_height = image.shape[0]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    start_y = 0
    split_heights = sorted(list(set([0] + heights + [img_height])))

    for i, end_y in enumerate(split_heights[1:]):
        img_slice = image[start_y:end_y, :]
        slice_path = os.path.join(output_dir, f"slice_{i}.png")
        cv2.imwrite(slice_path, img_slice)
        start_y = end_y

    return os.path.abspath(output_dir)


def split_and_save_image_pil(img: Image.Image, heights: list[int]) -> list[bytes]:
    """
    Splits a PIL image into multiple parts based on a list of heights.

    :param img: The input PIL image.
    :param heights: A list of integer heights to split the image at.
    :return: A list of bytes, where each element is a split image in PNG format.
    """
    img_height = img.height
    images = []

    start_y = 0
    split_heights = sorted(list(set([0] + heights + [img_height])))

    for end_y in split_heights[1:]:
        img_slice = img.crop((0, start_y, img.width, end_y))
        img_byte_arr = BytesIO()
        img_slice.save(img_byte_arr, format="PNG")
        images.append(img_byte_arr.getvalue())
        start_y = end_y

    return images


def main():
    parser = argparse.ArgumentParser(description="Split an image into multiple parts.")
    parser.add_argument("image_file", type=str, help="Path to the image file.")
    parser.add_argument(
        "--heights",
        type=int,
        nargs="+",
        required=True,
        help="A list of heights to split the image at.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="split_images",
        help="The directory to save the split images.",
    )
    args = parser.parse_args()

    try:
        # Read image as a byte stream to handle non-ASCII file paths
        img_data = np.fromfile(args.image_file, np.uint8)
        image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Image not found or could not be decoded at path: {args.image_file}")
    except Exception as e:
        raise IOError(f"Failed to read image file: {e}")

    result_path = split_and_save_image(image, args.heights, args.output_dir)
    print(f"Images saved to: {result_path}")


if __name__ == "__main__":
    main()

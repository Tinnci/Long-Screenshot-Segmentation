import cv2
import argparse
import os
import numpy as np


def draw_line_from_file(
    image_file: str,
    heights: list[int],
    color: tuple[int, int, int] = (0, 0, 255),
    output_dir: str = "result",
) -> str:
    """
    Draws horizontal lines on an image at specified heights and saves it.

    :param image_file: Path to the image file.
    :param heights: A list of integer heights where the lines will be drawn.
    :param color: The color of the lines in BGR format.
    :param output_dir: The directory to save the output image.
    :return: The absolute path to the saved image.
    """
    try:
        # Read image as a byte stream to handle non-ASCII file paths
        img_data = np.fromfile(image_file, np.uint8)
        image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(
                f"Image not found or could not be decoded at path: {image_file}"
            )
    except Exception as e:
        raise IOError(f"Failed to read image file: {e}")

    for height in heights:
        cv2.line(image, (0, height), (image.shape[1], height), color, 2)

    os.makedirs(output_dir, exist_ok=True)
    base_name, ext = os.path.splitext(os.path.basename(image_file))
    output_filename = f"{base_name}_result{ext}"
    output_path = os.path.join(output_dir, output_filename)

    # Use imencode + binary write to handle Unicode filenames
    success, encoded_img = cv2.imencode(ext if ext else ".jpg", image)
    if success:
        with open(output_path, "wb") as f:
            f.write(encoded_img)
    else:
        raise IOError(f"Failed to encode image for writing to {output_path}")

    return os.path.abspath(output_path)


def draw_line(
    image: np.ndarray, heights: list[int], color: tuple[int, int, int] = (0, 0, 255)
) -> np.ndarray:
    """
    Draws horizontal lines on an image.

    :param image: The input image as a NumPy array.
    :param heights: A list of integer heights where the lines will be drawn.
    :param color: The color of the lines in BGR format.
    :return: The image with the lines drawn.
    """
    for height in heights:
        cv2.line(image, (0, height), (image.shape[1], height), color, 2)
    return image


def main():
    parser = argparse.ArgumentParser(description="Draw lines on an image.")
    parser.add_argument("image_file", type=str, help="Path to the image file.")
    parser.add_argument(
        "--heights",
        type=int,
        nargs="+",
        required=True,
        help="A list of heights to draw lines at.",
    )
    parser.add_argument(
        "--color",
        type=str,
        default="0,0,255",
        help="The color of the lines in B,G,R format (e.g., '0,0,255' for red).",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="result",
        help="The directory to save the output image.",
    )
    args = parser.parse_args()

    try:
        color = tuple(map(int, args.color.split(",")))
        if len(color) != 3:
            raise ValueError("Color must be three comma-separated integers.")
    except ValueError as e:
        raise ValueError(f"Invalid color format: {e}") from e

    result_path = draw_line_from_file(
        args.image_file, args.heights, color, args.output_dir
    )
    print(f"Image saved to: {result_path}")


if __name__ == "__main__":
    main()

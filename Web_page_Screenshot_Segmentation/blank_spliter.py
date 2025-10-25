import cv2
import numpy as np


def find_low_variation_regions(
    image: np.ndarray, height_threshold: int, variation_threshold: float
) -> list[tuple[int, int]]:
    """
    Finds regions in an image with low vertical variation.

    This function scans an image from top to bottom and identifies contiguous
    regions where the vertical variation (Laplacian variance) is below a
    certain threshold.

    :param image: The input image as a NumPy array.
    :param height_threshold: The minimum height of a region to be considered.
    :param variation_threshold: The variance threshold to determine low variation.
    :return: A list of tuples, where each tuple contains the start and end
             row of a low variation region.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    regions = []
    start_row = None

    for i in range(gray.shape[0]):
        row_variation = cv2.Laplacian(gray[i : i + 1, :], cv2.CV_64F).var()
        if row_variation < variation_threshold:
            if start_row is None:
                start_row = i
        else:
            if start_row is not None and (i - start_row) >= height_threshold:
                regions.append((start_row, i))
            start_row = None

    if start_row is not None and (gray.shape[0] - start_row) >= height_threshold:
        regions.append((start_row, gray.shape[0]))

    return regions


def find_height_spliter(
    image: np.ndarray, height_threshold: int, variation_threshold: float
) -> list[int]:
    """
    Finds split points in an image based on low variation regions.

    This function identifies low variation regions and returns their vertical
    midpoints as potential split points.

    :param image: The input image as a NumPy array.
    :param height_threshold: The minimum height of a region to be considered.
    :param variation_threshold: The variance threshold to determine low variation.
    :return: A list of integer heights representing the midpoints of low
             variation regions.
    """
    regions = find_low_variation_regions(image, height_threshold, variation_threshold)
    return [start + (end - start) // 2 for start, end in regions]

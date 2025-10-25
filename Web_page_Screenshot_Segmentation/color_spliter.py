import cv2
import numpy as np


def color_height_spliter(
    image: np.ndarray, var_color_threshold: float, color_difference_threshold: float
) -> list[int]:
    """
    Finds split points in an image based on color differences between rows.

    This function analyzes an image to find horizontal split points by identifying
    rows with low color variance and significant color differences from the
    previous row.

    :param image: The input image as a NumPy array.
    :param var_color_threshold: The variance threshold to identify low-variance rows.
    :param color_difference_threshold: The minimum color difference to consider
                                       a split point.
    :return: A list of integer heights representing the potential split points.
    """
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate row-wise variance and mean using NumPy
    row_vars = np.var(image_gray, axis=1)
    row_means = np.mean(image_gray, axis=1)

    height_list = []
    previous_row_color = None

    for i in range(len(row_vars)):
        if row_vars[i] < var_color_threshold:
            if previous_row_color is not None:
                color_difference = np.linalg.norm(row_means[i] - previous_row_color)
                if color_difference > color_difference_threshold:
                    height_list.append(i)
            previous_row_color = row_means[i]

    return height_list

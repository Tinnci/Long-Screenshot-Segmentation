import logging
import time
import cv2
from Web_page_Screenshot_Segmentation.blank_spliter import find_low_variation_regions

logging.basicConfig(level=logging.DEBUG)  # Use standard logging


def display_regions(image, regions):
    # Output and mark results
    for start, end in regions:
        logging.debug(f"Found a low variation region from row {start} to {end}")
        cv2.rectangle(image, (0, start), (image.shape[1], end), (0, 255, 0), 2)


def on_trackbar_change(_):
    # Create a copy of the original image
    img_copy = original_image.copy()
    # Get current slider positions as parameters
    height_threshold = cv2.getTrackbarPos("Height Threshold", "Image")
    variation_threshold = cv2.getTrackbarPos("Variation Threshold", "Image") / 100

    # Reprocess the image with new parameters
    regions = find_low_variation_regions(
        img_copy, height_threshold, variation_threshold
    )
    display_regions(img_copy, regions)
    cv2.imwrite(f"{time.time()}.jpg", img_copy)
    # Display the processed image
    # cv2.resizeWindow('Image', 720, 2000)
    cv2.imshow("Image", img_copy)


# Read original image
original_image = cv2.imread(r"../imgs/ycwaterjet_cut.jpeg")

# Create window and sliders
cv2.namedWindow("Image")
cv2.createTrackbar("Height Threshold", "Image", 100, 500, on_trackbar_change)
cv2.createTrackbar("Variation Threshold", "Image", 50, 100, on_trackbar_change)
# cv2.resizeWindow('Image', 100, 300)
# Initial image processing
on_trackbar_change(0)

# Wait for user interaction or window close
cv2.waitKey(0)
cv2.destroyAllWindows()

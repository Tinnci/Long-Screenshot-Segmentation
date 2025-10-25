"""Unit tests for Web_page_Screenshot_Segmentation.color_spliter module."""

import pytest
import cv2
import numpy as np
from Web_page_Screenshot_Segmentation.color_spliter import color_height_spliter


class TestColorSpliter:
    """Tests for color_spliter functions."""

    @pytest.fixture
    def sample_image(self):
        """Create a sample image with color variations."""
        img = np.ones((1000, 500, 3), dtype=np.uint8) * 255
        # Add a region with different color
        img[200:400, :] = [100, 100, 200]
        return img

    @pytest.mark.unit
    def test_color_height_spliter_returns_list(self, sample_image):
        """Test that color_height_spliter returns a list."""
        result = color_height_spliter(sample_image, 100, 15)
        assert isinstance(result, list)

    @pytest.mark.unit
    def test_color_height_spliter_with_different_thresholds(self, sample_image):
        """Test with different threshold values."""
        result1 = color_height_spliter(sample_image, 50, 15)
        result2 = color_height_spliter(sample_image, 100, 15)
        result3 = color_height_spliter(sample_image, 150, 15)

        # All should return lists
        assert isinstance(result1, list)
        assert isinstance(result2, list)
        assert isinstance(result3, list)

    @pytest.mark.unit
    def test_color_height_spliter_with_real_image(self, sample_image_path):
        """Test color_height_spliter with real image."""
        img_data = np.fromfile(sample_image_path, np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)

        result = color_height_spliter(img, 100, 15)
        assert isinstance(result, list)
        assert all(isinstance(h, (int, np.integer)) for h in result)

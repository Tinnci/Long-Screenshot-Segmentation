"""Unit tests for Web_page_Screenshot_Segmentation.blank_spliter module."""

import pytest
import cv2
import numpy as np
from Web_page_Screenshot_Segmentation.blank_spliter import (
    find_low_variation_regions,
    find_height_spliter,
)


class TestBlankSpliter:
    """Tests for blank_spliter functions."""

    @pytest.fixture
    def sample_image(self):
        """Create a sample image for testing."""
        # Create a test image with vertical blank regions
        img = np.ones((1000, 500, 3), dtype=np.uint8) * 255
        # Add a non-blank region in the middle
        img[200:400, :] = [100, 100, 100]
        return img

    @pytest.mark.unit
    def test_find_low_variation_regions_returns_list(self, sample_image):
        """Test that find_low_variation_regions returns a list."""
        result = find_low_variation_regions(sample_image, 100, 0.5)
        assert isinstance(result, list)

    @pytest.mark.unit
    def test_find_low_variation_regions_with_different_thresholds(self, sample_image):
        """Test with different threshold values."""
        result1 = find_low_variation_regions(sample_image, 50, 0.5)
        result2 = find_low_variation_regions(sample_image, 100, 0.5)
        result3 = find_low_variation_regions(sample_image, 200, 0.5)

        # All should return lists
        assert isinstance(result1, list)
        assert isinstance(result2, list)
        assert isinstance(result3, list)

    @pytest.mark.unit
    def test_find_height_spliter_returns_list(self, sample_image):
        """Test that find_height_spliter returns a list."""
        result = find_height_spliter(sample_image, 100, 0.5)
        assert isinstance(result, list)

    @pytest.mark.unit
    def test_find_height_spliter_with_real_image(self, sample_image_path):
        """Test find_height_spliter with real image."""
        img_data = np.fromfile(sample_image_path, np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)

        result = find_height_spliter(img, 102, 0.5)
        assert isinstance(result, list)
        assert all(isinstance(h, (int, np.integer)) for h in result)

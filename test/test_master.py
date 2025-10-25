"""Unit tests for Web_page_Screenshot_Segmentation.master module."""

import pytest
import numpy as np
from Web_page_Screenshot_Segmentation.master import split_heights, remove_close_values


class TestRemoveCloseValues:
    """Tests for the remove_close_values helper function."""

    def test_remove_close_values_empty_list(self):
        """Empty list should return empty list."""
        result = remove_close_values([], 100)
        assert result == []

    def test_remove_close_values_single_value(self):
        """Single value should be preserved."""
        result = remove_close_values([500], 100)
        assert result == [500]

    def test_remove_close_values_filters_by_threshold(self):
        """Values closer than threshold should be removed."""
        values = [100, 150, 400, 420, 800]
        result = remove_close_values(values, 100, min_height=50)
        # With min_height=50: [100, 150, 400, 420, 800]
        # 100, 400 (>300 away), 800 (>300 away) should be kept
        assert result == [100, 400, 800]

    def test_remove_close_values_filters_min_height(self):
        """Values below min_height should be removed."""
        values = [50, 100, 500, 1000]
        result = remove_close_values(values, 50, min_height=200)
        assert result == [500, 1000]

    def test_remove_close_values_sorts_input(self):
        """Input list should be sorted."""
        values = [800, 200, 500, 100]
        result = remove_close_values(values, 100)
        # Should be sorted: [100, 200, 500, 800]
        assert result == sorted(result)


class TestSplitHeights:
    """Tests for the split_heights function."""

    @pytest.mark.unit
    def test_split_heights_with_unicode_filename(self, unicode_image_path):
        """Test that split_heights can handle Unicode file paths."""
        result = split_heights(unicode_image_path)
        
        # Should return a list of integers (split heights)
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(h, (int, np.integer)) for h in result)

    @pytest.mark.unit
    def test_split_heights_returns_list(self, sample_image_path):
        """Test that split_heights returns a list of integers."""
        result = split_heights(sample_image_path)
        
        assert isinstance(result, list)
        assert all(isinstance(h, (int, np.integer)) for h in result)

    @pytest.mark.unit
    def test_split_heights_invalid_path_raises_error(self):
        """Test that invalid path raises IOError."""
        with pytest.raises(IOError):
            split_heights("/nonexistent/path/image.png")

    @pytest.mark.unit
    def test_split_heights_with_split_option(self, sample_image_path, tmp_path):
        """Test that split option saves output image."""
        output_dir = str(tmp_path / "output")
        result = split_heights(sample_image_path, split=True, output_dir=output_dir)
        
        # Should return path string when split=True
        assert isinstance(result, str)
        assert result.endswith("_result.jpg")
        # Output file should exist (check for file in directory since unicode handling may vary)
        output_files = list(Path(output_dir).glob("*_result.jpg"))
        assert len(output_files) > 0, f"No _result.jpg files found in {output_dir}"

    @pytest.mark.unit
    def test_split_heights_parameters(self, sample_image_path):
        """Test that custom parameters are accepted."""
        # Should not raise with custom parameters
        result = split_heights(
            sample_image_path,
            height_threshold=150,
            variation_threshold=0.3,
            color_threshold=120,
            color_variation_threshold=20,
            merge_threshold=400,
        )
        
        assert isinstance(result, list)


# Import Path for file existence check
from pathlib import Path

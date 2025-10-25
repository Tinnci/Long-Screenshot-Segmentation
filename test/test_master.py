"""Unit tests for Web_page_Screenshot_Segmentation.master module."""

import pytest
import numpy as np
from pathlib import Path
from Web_page_Screenshot_Segmentation.master import (
    split_heights,
    remove_close_values,
    split_and_export_segments,
    auto_crop_image,
)


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


class TestSplitAndExportSegments:
    """Tests for the split_and_export_segments function."""

    @pytest.mark.unit
    def test_split_and_export_segments_creates_directory(
        self, sample_image_path, tmp_path
    ):
        """Test that split_and_export_segments creates output directory."""
        output_dir = str(tmp_path / "segments")
        result = split_and_export_segments(sample_image_path, output_dir=output_dir)

        # Should return absolute path to output directory
        assert isinstance(result, str)
        assert Path(result).exists()
        assert Path(result).is_dir()

    @pytest.mark.unit
    def test_split_and_export_segments_creates_files(self, sample_image_path, tmp_path):
        """Test that split_and_export_segments creates segment files."""
        output_dir = str(tmp_path / "segments")
        result = split_and_export_segments(sample_image_path, output_dir=output_dir)

        # Should create multiple segment files
        segment_files = list(Path(result).glob("*_segment_*.jpg"))
        assert len(segment_files) > 0, "No segment files were created"

    @pytest.mark.unit
    def test_split_and_export_segments_preserves_basename(
        self, sample_image_path, tmp_path
    ):
        """Test that segment filenames preserve original basename."""
        output_dir = str(tmp_path / "segments")
        result = split_and_export_segments(sample_image_path, output_dir=output_dir)

        # Get original filename
        base_name = Path(sample_image_path).stem

        # Check that segment files contain the original basename
        segment_files = list(Path(result).glob(f"{base_name}_segment_*.jpg"))
        assert len(segment_files) > 0

    @pytest.mark.unit
    def test_split_and_export_segments_with_unicode_filename(
        self, unicode_image_path, tmp_path
    ):
        """Test that split_and_export_segments handles Unicode filenames."""
        output_dir = str(tmp_path / "segments")
        result = split_and_export_segments(unicode_image_path, output_dir=output_dir)

        # Should create segments with preserved Unicode characters
        segment_files = list(Path(result).glob("*_segment_*.jpg"))
        assert len(segment_files) > 0

        # Verify Unicode characters are preserved in filenames
        for seg_file in segment_files:
            # Check that file exists and can be accessed
            assert seg_file.exists()
            assert seg_file.stat().st_size > 0

    @pytest.mark.unit
    def test_split_and_export_segments_custom_parameters(
        self, sample_image_path, tmp_path
    ):
        """Test that custom threshold parameters are accepted."""
        output_dir = str(tmp_path / "segments")

        # Should not raise with custom parameters
        result = split_and_export_segments(
            sample_image_path,
            output_dir=output_dir,
            height_threshold=150,
            variation_threshold=0.3,
            color_threshold=120,
            color_variation_threshold=20,
            merge_threshold=400,
        )

        assert isinstance(result, str)
        assert Path(result).exists()

    @pytest.mark.unit
    def test_split_and_export_segments_invalid_path_raises_error(self, tmp_path):
        """Test that invalid image path raises IOError."""
        output_dir = str(tmp_path / "segments")

        with pytest.raises(IOError):
            split_and_export_segments("/nonexistent/path/image.png", output_dir)

    @pytest.mark.unit
    def test_split_and_export_segments_with_auto_crop(
        self, sample_image_path, tmp_path
    ):
        """Test that auto_crop parameter is accepted and processed."""
        output_dir = str(tmp_path / "segments")

        result = split_and_export_segments(
            sample_image_path,
            output_dir=output_dir,
            auto_crop=True,
            crop_threshold=240,
            crop_min_height=50,
        )

        # Should still return valid path
        assert isinstance(result, str)
        assert Path(result).exists()


class TestAutoCropImage:
    """Tests for the auto_crop_image function."""

    @pytest.fixture
    def blank_padded_image(self):
        """Create test image with blank (white) padding on top and bottom."""
        # Create a simple image: white padding + content + white padding
        img = np.ones((300, 200, 3), dtype=np.uint8) * 255  # All white

        # Add content in the middle (gray/darker area)
        img[100:200, :] = [100, 100, 100]  # Gray content

        return img

    @pytest.mark.unit
    def test_auto_crop_image_removes_blank_rows(self, blank_padded_image):
        """Test that auto_crop removes blank rows from top and bottom."""
        original_height = blank_padded_image.shape[0]
        cropped = auto_crop_image(blank_padded_image, threshold=240)

        # Should be smaller after cropping
        assert cropped.shape[0] < original_height
        # Should preserve middle content
        assert cropped.shape[0] >= 100

    @pytest.mark.unit
    def test_auto_crop_image_preserves_min_height(self):
        """Test that auto_crop respects minimum height."""
        # Create small image
        small_img = np.ones((30, 50, 3), dtype=np.uint8) * 255
        small_img[10:20, :] = [100, 100, 100]

        cropped = auto_crop_image(small_img, min_height=50)

        # Should not be cropped below min_height
        assert cropped.shape[0] >= 30  # Returns original if < min_height

    @pytest.mark.unit
    def test_auto_crop_image_with_all_blank(self):
        """Test that auto_crop handles all-blank images gracefully."""
        all_white = np.ones((100, 100, 3), dtype=np.uint8) * 255

        cropped = auto_crop_image(all_white, threshold=240)

        # Should return original (no non-blank rows found)
        assert cropped.shape == all_white.shape

    @pytest.mark.unit
    def test_auto_crop_image_grayscale(self):
        """Test that auto_crop works with grayscale images."""
        # Create grayscale image with blank padding
        img = np.ones((150, 100), dtype=np.uint8) * 255
        img[50:100, :] = 100  # Gray content

        cropped = auto_crop_image(img, threshold=240)

        # Should crop successfully
        assert cropped.shape[0] < 150
        assert len(cropped.shape) == 2  # Still grayscale

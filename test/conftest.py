"""Pytest configuration and fixtures for Web_page_Screenshot_Segmentation tests."""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_images_dir():
    """Provide path to test images directory."""
    return Path(__file__).parent.parent / "images"


@pytest.fixture
def sample_image_path(test_images_dir):
    """Provide path to a sample image for testing."""
    # Look for the Chinese filename image that was tested
    chinese_image = test_images_dir / "16、奈氏图绘制.png"
    if chinese_image.exists():
        return str(chinese_image)

    # Fallback to any PNG file in the directory
    for img_file in test_images_dir.glob("*.png"):
        return str(img_file)

    # Fallback to any JPEG file
    for img_file in test_images_dir.glob("*.jpeg"):
        return str(img_file)
    for img_file in test_images_dir.glob("*.jpg"):
        return str(img_file)

    pytest.skip("No test images found in images directory")


@pytest.fixture
def unicode_image_path(test_images_dir):
    """Provide path to image with Unicode characters in filename."""
    chinese_image = test_images_dir / "16、奈氏图绘制.png"
    if not chinese_image.exists():
        pytest.skip("Unicode filename test image not found")
    return str(chinese_image)

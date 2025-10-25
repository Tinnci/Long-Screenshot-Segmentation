# Release Notes v1.1.0

**Release Date:** October 25, 2025  
**Tag:** `V1.1.0`  
**Commits:** 4eeafa0  

## 🎉 Major Changes

### ✅ Fixed: Unicode Filename Support on Windows
- **Issue:** The tool failed to process images with non-ASCII characters (e.g., Chinese punctuation) in filenames on Windows
- **Root Cause:** OpenCV's `cv2.imread()` has limited Unicode path support on Windows
- **Solution:** Replaced `cv2.imread(path)` with `np.fromfile(path, np.uint8)` + `cv2.imdecode()` pattern
- **Files Modified:**
  - `Web_page_Screenshot_Segmentation/master.py`
  - `Web_page_Screenshot_Segmentation/drawer.py`
  - `Web_page_Screenshot_Segmentation/spliter.py`
- **Testing:** Verified with real image: `16、奈氏图绘制.png` ✓

### ✨ New: Comprehensive Pytest Test Suite
- **17 Unit Tests** covering all major functionality
- **Test Coverage:**
  - `test_master.py` — 10 tests (split height detection, parameter validation)
  - `test_blank_spliter.py` — 4 tests (blank region detection)
  - `test_color_spliter.py` — 3 tests (color-based splitting)
- **Fixtures:** Automatic test image discovery and Unicode path support testing
- **Coverage Report:** 57% overall, **100% for core algorithms**

### 📊 Code Quality Improvements
- Applied **Ruff** formatter to all Python files
- Fixed all linting issues (F401, E402)
- Removed unused imports
- 100% clean: `ruff check` and `ruff format` passing

### 📚 Documentation
- **README_TESTING.md** — Complete testing guide with examples
- **PYTEST_SETUP.md** — Setup summary and quick reference
- **Enhanced .gitignore** — Comprehensive patterns for Python, IDEs, OS, and project-specific files

### ⚙️ Configuration
- Added pytest config to `pyproject.toml`:
  - Test discovery patterns
  - Markers for test categorization (unit, integration, slow)
  - Coverage settings
- Added dev dependencies: `pytest>=7.0`, `pytest-cov>=4.0`

## 📋 Version Summary

| Component | Status |
|-----------|--------|
| Unicode Filename Support | ✅ Fixed |
| Test Suite | ✅ 17/17 Passing |
| Code Coverage | ✅ 57% Overall |
| Core Algorithm Coverage | ✅ 100% |
| Linting | ✅ All Clean |
| Formatting | ✅ Applied |
| Documentation | ✅ Complete |

## 🚀 Installation & Usage

### Install Latest Version
```bash
uv tool install web-page-screenshot-segmentation --upgrade
```

### Use with Unicode Filenames (New!)
```bash
# Now works with Chinese, Japanese, or any Unicode characters
screenshot-segment -f "C:\path\to\图片.png"
screenshot-draw -f "C:\path\to\イメージ.png"
screenshot-split -f "C:\path\to\εικόνα.png"
```

### Run Tests
```bash
# Setup virtual environment
uv venv
.venv\Scripts\activate

# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest -v
pytest --cov=Web_page_Screenshot_Segmentation --cov-report=html
```

## 🔄 Backward Compatibility

✅ **Fully Backward Compatible** — No breaking changes  
✅ No migration needed  
✅ All previous versions' features still work  
✅ API unchanged

## 🐛 Known Issues

None at this release.

## 📝 Commits Included

```
4eeafa0 chore: Bump version to 1.1.0
c3cb28d chore: Complete and enhance .gitignore
1fdd123 style: Apply ruff formatting and fix linting issues
d97cd2b feat: Fix Unicode filename support and add comprehensive pytest suite
```

## 👤 Contributors

- [@shiso](https://github.com/shiso)

## 📞 Support

- See [README_TESTING.md](README_TESTING.md) for testing documentation
- See [PYTEST_SETUP.md](PYTEST_SETUP.md) for setup instructions
- Check [README.md](README.md) for general usage

---

**Next Steps:**
- `git push origin main` — Push commits to remote
- `git push origin V1.1.0` — Push tag to remote

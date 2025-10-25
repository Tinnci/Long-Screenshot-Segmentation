# Publishing to PyPI

This guide explains how to publish the long-screenshot-segmentation package to PyPI.

**Good news:** Your project is already well-configured for PyPI! This process is straightforward and takes ~10 minutes.

## Prerequisites

### 1. PyPI Account

Create an account at https://pypi.org/account/register/

### 2. API Token

1. Log in to PyPI
2. Go to https://pypi.org/manage/account/#api-tokens
3. Click "Create new token"
4. Choose scope: "Entire account" or "Only this project" (project-specific is recommended)
5. Copy the token - you'll need it soon

**Token Format:** `pypi-AgEIcHlwaS5vcmc...` (it starts with `pypi-`)

### 3. Build Tools

Install the necessary tools:

```bash
pip install build twine

# Or with uv (recommended)
uv pip install build twine
```

## Publishing Steps

### Step 1: Verify Your Package

Test the build locally to catch any issues:

```bash
# Clean previous builds
rm -r build/ dist/ *.egg-info/

# Build the package
python -m build

# Check the build (optional but recommended)
twine check dist/*
```

This creates:
- `dist/long_screenshot_segmentation-1.1.0-py3-none-any.whl` (wheel)
- `dist/long-screenshot-segmentation-1.1.0.tar.gz` (source distribution)

### Step 2: Upload to PyPI

**Option A: Interactive (First Time)**

```bash
twine upload dist/*
```

When prompted for username, enter: `__token__`
When prompted for password, paste your API token

**Option B: Using .pypirc Configuration (Recommended)**

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...PASTE_YOUR_TOKEN_HERE...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...test-token...
```

Then upload:

```bash
twine upload dist/*
```

**Option C: Environment Variable (CI/CD)**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...
twine upload dist/*
```

### Step 3: Verify Upload

1. Visit https://pypi.org/project/long-screenshot-segmentation/
2. Confirm your package appears
3. Test installation:

```bash
pip install long-screenshot-segmentation==1.1.0
```

## Testing on TestPyPI First (Optional but Recommended)

TestPyPI is a safe environment to test before uploading to the real PyPI:

```bash
# Create test token at https://test.pypi.org/manage/account/#api-tokens

# Upload to test
twine upload -r testpypi dist/*

# Install from test
pip install -i https://test.pypi.org/simple/ long-screenshot-segmentation==1.1.0
```

## For Future Updates

When you make changes and want to release a new version:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.2.0"
   ```

2. **Create git tag** (optional but recommended):
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

3. **Rebuild and upload**:
   ```bash
   rm -r build/ dist/ *.egg-info/
   python -m build
   twine upload dist/*
   ```

## CI/CD: Automated Publishing with GitHub Actions

To automatically publish when you create a release, add `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install build tools
        run: pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Then:
1. Go to repo Settings → Secrets and variables → Actions
2. Create secret: `PYPI_API_TOKEN` with your token value
3. Create a release on GitHub → Auto-publishes to PyPI! 🎉

## Troubleshooting

### Error: "Invalid authentication"
- Check token is correct (starts with `pypi-`)
- Verify username is `__token__` (not your username)

### Error: "File already exists"
- Each version can only be uploaded once
- Increment version in `pyproject.toml` and rebuild

### Error: "long_description_content_type"
- Ensure `readme = "README.md"` in `pyproject.toml` ✓ (You have this!)

### Package not installing
- Check on https://pypi.org/project/long-screenshot-segmentation/
- PyPI caches for ~5 minutes; try again later
- Verify CLI commands work: `screenshot-segment --help`

## Current Project Status

✅ **Ready for PyPI:**
- Proper `pyproject.toml` configuration
- Clear dependencies with versions
- Comprehensive README.md
- MIT license
- CLI entry points configured
- Well-tested (28 tests)

**Next steps:**
1. Create PyPI account
2. Generate API token
3. Run `python -m build && twine upload dist/*`
4. Done! 🚀

## References

- PyPI: https://pypi.org/
- Packaging Guide: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/

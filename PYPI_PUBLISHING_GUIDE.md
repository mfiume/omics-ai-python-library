# PyPI Publishing Guide

This guide explains how to publish the `omics-ai-explorer` package to PyPI.

## 🚀 **Package Status: READY FOR PYPI**

✅ **All prerequisites completed:**
- Modern `pyproject.toml` configuration
- Comprehensive test suite (8 tests passing)
- Distribution packages built and validated
- Documentation and examples included
- GitHub repository published

## 📦 **Current Build Artifacts**

The following distribution files are ready in `dist/`:
- `omics_ai_explorer-0.1.0-py3-none-any.whl` (universal wheel)
- `omics_ai_explorer-0.1.0.tar.gz` (source distribution)

Both packages have been validated with `twine check` ✅

## 🔑 **Prerequisites for Publishing**

### 1. Create PyPI Account
- Register at https://pypi.org/account/register/
- Verify your email address
- Enable two-factor authentication (recommended)

### 2. Create Test PyPI Account (Optional but Recommended)
- Register at https://test.pypi.org/account/register/
- This allows testing the upload process safely

### 3. Generate API Tokens
- Go to PyPI Account Settings → API tokens
- Create a new API token for this project
- Copy the token (starts with `pypi-`)
- Store it securely (you won't see it again)

## 📤 **Publishing Steps**

### Step 1: Test Upload (Recommended)
```bash
# Activate virtual environment
source test_env/bin/activate

# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: <your-test-pypi-token>
```

### Step 2: Verify Test Installation
```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ omics-ai-explorer

# Test the installation
python -c "from omics_ai import OmicsAIClient; print('✅ Test PyPI package works!')"
```

### Step 3: Production Upload
```bash
# Upload to production PyPI
twine upload dist/*

# When prompted:
# Username: __token__  
# Password: <your-pypi-token>
```

### Step 4: Verify Production Installation
```bash
# Install from PyPI
pip install omics-ai-explorer

# Test the installation
python -c "from omics_ai import OmicsAIClient; print('✅ Production package works!')"
```

## 🔧 **Alternative: Using API Token Files**

Create a `.pypirc` file in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-test-pypi-token>
```

Then upload with:
```bash
twine upload --repository testpypi dist/*  # For test
twine upload dist/*                        # For production
```

## 🔄 **Future Releases**

For version updates:

### 1. Update Version
Edit `pyproject.toml`:
```toml
version = "0.1.1"  # or next version
```

### 2. Update Changelog
Add new section to `CHANGELOG.md`:
```markdown
## [0.1.1] - YYYY-MM-DD
### Added
- New feature description
### Fixed
- Bug fix description
```

### 3. Rebuild and Upload
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Rebuild
python -m build

# Check packages
twine check dist/*

# Upload
twine upload dist/*
```

## 🛡️ **Security Best Practices**

1. **Never commit API tokens** to version control
2. **Use scoped tokens** specific to this project
3. **Enable 2FA** on your PyPI account
4. **Test uploads** on Test PyPI first
5. **Keep tokens secure** and rotate them periodically

## 📊 **Package Information**

- **Package Name**: `omics-ai-explorer`
- **Current Version**: `0.1.0`
- **Author**: Marc Fiume
- **License**: MIT
- **Python Support**: >=3.7
- **Dependencies**: `requests>=2.25.0`

## 🎯 **Expected Outcome**

After successful upload, users will be able to install with:
```bash
pip install omics-ai-explorer
```

And use it like:
```python
from omics_ai import OmicsAIClient

client = OmicsAIClient("hifisolves")
collections = client.list_collections()
```

## 🆘 **Troubleshooting**

### Common Issues:

1. **403 Forbidden**: Check your API token and permissions
2. **400 Bad Request**: Verify package metadata in `pyproject.toml`  
3. **File exists**: Version already published, increment version number
4. **Network errors**: Check internet connection and PyPI status

### Package Validation:
```bash
# Re-check packages before upload
twine check dist/*

# Verify package contents
tar -tzf dist/omics_ai_explorer-0.1.0.tar.gz
unzip -l dist/omics_ai_explorer-0.1.0-py3-none-any.whl
```

## 📋 **Post-Publishing Checklist**

- [ ] Verify package appears on PyPI
- [ ] Test installation in clean environment
- [ ] Update README badges (if applicable)
- [ ] Announce release
- [ ] Monitor for issues/feedback

---

**Ready to publish!** 🚀

The package is fully prepared and tested. Follow the steps above to make `omics-ai-explorer` available to the Python community.
# Installation Guide - Choose Your Method

This guide explains three ways to install and run the F&B Recommendation System.

---

## Method 1: UV (Recommended - Fastest)

UV is a modern, fast Python package manager written in Rust. **Perfect for assignments.**

### Prerequisites
- Python 3.14+ installed
- UV installed from https://docs.astral.sh/uv/

### Installation Steps

```bash
# Navigate to project
cd assignment_package_canteen_rep

# One command installs everything
uv sync
```

**What happens:**
- ✅ Creates `.venv` virtual environment
- ✅ Installs all dependencies
- ✅ Locks versions in `uv.lock`

### Run the App
```bash
uv run assignment.py
```

### Pros
- ⚡ Fastest installation
- 🔒 Reproducible (uv.lock ensures exact versions)
- ✨ Modern and actively maintained
- 📦 Automatically manages virtual environment
- Perfect for CI/CD and automated testing

### Cons
- Requires separate UV installation

---

## Method 2: Standard Python + pip (Most Compatible)

The traditional way using Python's built-in package manager.

### Prerequisites
- Python 3.14+ installed
- pip (comes with Python)

### Installation Steps

```bash
# Navigate to project
cd assignment_package_canteen_rep

# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App
```bash
python assignment.py
```

### Pros
- 🌍 Works everywhere Python is installed
- 🔧 No additional tools needed
- 📚 Well-documented and widely understood
- ✅ Maximum compatibility

### Cons
- ⏱️ Slower than UV
- No automatic version locking

---

## Method 3: Manual Installation from pyproject.toml

For advanced users who want full control.

### Prerequisites
- Python 3.14+ installed
- pip installed

### Installation Steps

```bash
# Navigate to project
cd assignment_package_canteen_rep

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install each dependency
pip install pygame==2.6.1
pip install pandas==2.3.3
pip install openpyxl==3.1.5
pip install pillow==11.3.0
```

### Run the App
```bash
python assignment.py
```

### Pros
- 🎯 Maximum control over versions
- 📖 Learn exactly what's being installed

### Cons
- ❌ Manual and error-prone
- Requires looking up correct versions

---

## Comparison Table

| Feature | UV | pip + requirements.txt | Manual |
|---------|----|-----------------------|--------|
| Speed | ⚡⚡⚡ Fastest | ⚡⚡ Medium | ⚡ Slow |
| Ease | ⭐⭐⭐ Easiest | ⭐⭐ Medium | ⭐ Complex |
| Compatibility | ⭐⭐ Good | ⭐⭐⭐ Best | ⭐⭐⭐ Best |
| Version Lock | ⭐⭐⭐ Yes | ⭐ No | ❌ No |
| Dependencies File | pyproject.toml | requirements.txt | pyproject.toml |
| Virtual Env Auto | ✅ Yes | ❌ Manual | ❌ Manual |
| **Recommendation** | ✅ BEST | ⭐ Good | ❌ Not recommended |

---

## Verify Installation

After installation, verify everything works:

```bash
# Test import
uv run python -c "import pygame; import pandas; print('✅ All imports successful!')"

# Or with standard Python (after activation):
python -c "import pygame; import pandas; print('✅ All imports successful!')"
```

Expected output: `✅ All imports successful!`

---

## Troubleshooting

### "Python not found"
- Ensure Python 3.14+ is installed
- Verify it's in your PATH
- Try `python3 --version` if `python` doesn't work

### "UV not found"
- Install UV from https://docs.astral.sh/uv/getting-started/installation/
- Or use Method 2 (pip) instead

### "Virtual environment not activated"
Look for `(venv)` in your terminal prompt. If missing:

```bash
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### "ModuleNotFoundError: No module named 'pygame'"
Ensure:
1. Virtual environment is activated (check prompt)
2. Dependencies were installed successfully
3. Try reinstalling: `uv sync` or `pip install -r requirements.txt`

### On macOS with Apple Silicon (M1/M2/M3)
Pygame should work fine with automatic compilation. If you encounter issues:
```bash
# Use native Python (not Rosetta)
/opt/homebrew/bin/python3 --version
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | macOS 10.13+, Linux, Windows 10+ | Latest version |
| **Python** | 3.14 | 3.14+ |
| **RAM** | 512MB | 2GB+ |
| **Disk** | 1GB free | 2GB+ free |
| **Display** | 1024x768 | 1920x1080+ |

---

## First Time Setup Checklist

- [ ] Python 3.14+ installed (`python --version`)
- [ ] Navigated to project directory (`cd assignment_package_canteen_rep`)
- [ ] Chose installation method (UV recommended)
- [ ] Completed installation steps
- [ ] Verified installation works
- [ ] Run: `uv run assignment.py` or `python assignment.py`
- [ ] See main menu with 5 options
- [ ] ✅ Ready to use!

---

## Quick Reference

```bash
# UV method
cd assignment_package_canteen_rep
uv sync
uv run assignment.py

# pip method
cd assignment_package_canteen_rep
python -m venv venv
source venv/bin/activate  # macOS/Linux or venv\Scripts\activate on Windows
pip install -r requirements.txt
python assignment.py
```

---

## Next Steps

After successful installation:
1. Read `QUICKSTART.md` for 2-minute introduction
2. See `README.md` for detailed feature guide
3. Start exploring with `python assignment.py`

---

**Need help?** Check README.md's Troubleshooting section for more detailed solutions.

# Quick Start Guide

Get the F&B Recommendation System running in 2 minutes!

## Quick Start with UV (Fastest)

```bash
# 1. Navigate to project directory
cd assignment_package_canteen_rep

# 2. Install dependencies (one command)
uv sync

# 3. Run the application
uv run assignment.py
```

**That's it!** The app will start and show the main menu.

---

## Quick Start with Standard Python

```bash
# 1. Navigate to project directory
cd assignment_package_canteen_rep

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python assignment.py
```

---

## First Run - What to Expect

```
========================
F&B Recommendation Menu
1 -- Display Data
2 -- Keyword-based Search
3 -- Price-based Search
4 -- Location-based Search
5 -- Exit Program
========================
Enter option [1-5]:
```

### Try These First:

1. **Option 1** - See all available data
2. **Option 2** - Search for "chinese" to test keyword search
3. **Option 3** - Search for "spicy" within price $5.00
4. **Option 4** - Click on map to find nearest canteens
5. **Option 5** - Exit

---

## Minimum Requirements

- Python 3.14+
- ~500MB disk space
- Display: 1024x768+

---

## Stuck?

See the full README.md for:
- Detailed feature explanations
- Troubleshooting guide
- Available keywords list
- Function documentation

---

## Key Commands Reference

| Task | UV | Python |
|------|----|----|
| Install | `uv sync` | `pip install -r requirements.txt` |
| Run | `uv run assignment.py` | `python assignment.py` |
| Check syntax | `uv run python -m py_compile assignment.py` | `python -m py_compile assignment.py` |

---

**Ready?** Start with your preferred installation method above!

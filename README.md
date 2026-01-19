# F&B Recommendation System - NTU Campus Canteen Finder

A Python-based food and beverage recommendation system for NTU (Nanyang Technological University) campus canteens. This application helps users discover canteens and stalls based on keywords, price preferences, and location proximity.

## Features

- **Keyword-based Search**: Find stalls by food type, cuisine, and dietary preferences (e.g., "Halal", "Spicy", "Chinese")
- **Price-based Search**: Search for stalls within your budget using keyword filtering
- **Location-based Search**: Find the k-nearest canteens to two user locations on an interactive map
- **Interactive Map Interface**: Click on the NTU campus map to select user locations (powered by Arcade)
- **Data-driven Results**: All information sourced from Excel spreadsheet with comprehensive canteen and stall data

## Technology Stack

- **Language**: Python 3.14+
- **UI Framework**: Arcade 3.3.3 (for interactive map)
- **Data Processing**: Pandas 2.3.3, OpenPyXL 3.1.5
- **Image Processing**: Pillow 11.3.0
- **Package Manager**: UV (optional, but recommended)

## Installation

### Option 1: Using UV (Recommended)

UV is a fast Python package installer and resolver. It's recommended for faster dependency installation.

**Prerequisites:**
- Python 3.14+ installed
- UV installed ([install UV](https://docs.astral.sh/uv/getting-started/installation/))

**Steps:**

1. Clone or download the project:
```bash
cd assignment_package_canteen_rep
```

2. Install dependencies with UV:
```bash
uv sync
```

This will:
- Read `pyproject.toml`
- Install all required dependencies
- Create a virtual environment (`.venv`)
- Lock dependencies in `uv.lock`

### Option 2: Using Standard Python

**Prerequisites:**
- Python 3.14+ installed
- pip (usually comes with Python)

**Steps:**

1. Clone or download the project:
```bash
cd assignment_package_canteen_rep
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install dependencies from `pyproject.toml`:
```bash
pip install arcade==3.3.3 pandas==2.3.3 openpyxl==3.1.5 pillow==11.3.0
```

Or create a `requirements.txt` file with these contents and run:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Using UV (Recommended)

```bash
uv run assignment.py
```

This will automatically use the project's virtual environment and run the application.

### Option 2: Using Standard Python

**After activating your virtual environment:**

```bash
python assignment.py
```

## Usage Guide

When you run the application, you'll see the main menu:

```
========================
F&B Recommendation Menu
1 -- Display Data
2 -- Keyword-based Search
3 -- Price-based Search
4 -- Location-based Search
5 -- Exit Program
========================
```

### Menu Options

#### Option 1: Display Data
Shows all available:
- Keyword dictionary (canteen → stall → food types)
- Price dictionary (canteen → stall → prices)
- Location dictionary (canteen → coordinates)

#### Option 2: Keyword-based Search
Search for stalls by food keywords.

**Example:**
```
Enter option [1-5]: 2
Enter food keywords (comma-separated): chinese, halal

Search Results:

Food Court 1:
  - Kee Chicken Rice: Chinese, Chicken, Rice

Food Court 16:
  - 16 Kitchen: Chinese, Western, Indian, Malay
```

**Available Keywords:**
- **Cuisine**: Chinese, Western, Indian, Malay, Japanese, Korean, Thai, Vietnamese
- **Dietary**: Spicy, Halal
- **Food Type**: Fries, Burgers, Chicken, Rice, Waffles, Noodles, Soups, Salads, Desserts, Hotpot

#### Option 3: Price-based Search
Search for stalls by keywords AND maximum price.

**Example:**
```
Enter option [1-5]: 3
Enter food keywords (comma-separated): chicken
Enter maximum price: 5.0

Search Results (within budget):

Food Court 1:
  - Kee Chicken Rice: Chinese, Chicken, Rice | Price: $3.50
```

#### Option 4: Location-based Search
Find the k-nearest canteens to two user locations.

**How it works:**
1. Select option 4
2. An interactive map window opens
3. Click to select User A's location (a pin will appear)
4. Click again to select User B's location
5. Window closes automatically
6. Enter the number of nearest canteens you want to find (k)
7. Results show the k-nearest canteens with distances

**Example:**
```
Enter option [1-5]: 4
Click on the map to select both user locations...
[Interactive map window opens]
[Click User A location] → Pin placed
[Click User B location] → Pin placed
User A's location (x, y): (396, 265)
User B's location (x, y): (274, 371)
Enter number of nearest canteens to find: 3
3 Nearest Canteens found:
Food Court 13 – 151m
Food Court 14 – 207m
Food Court 16 – 272m
```

**Important Notes for Location-based Search:**
- The arcade/map interface can only be used once per program session (library limitation)
- If you need to use it again, restart the program (select option 5, then run again)
- Distance is measured as Euclidean distance from the midpoint of the two user locations
- k defaults to 1 if invalid or negative value is entered

#### Option 5: Exit Program
Closes the application.

## File Structure

```
assignment_package_canteen_rep/
├── assignment.py              # Main application file
├── main.py                    # Entry point (optional)
├── canteens.xlsx              # Data file with canteen/stall information
├── NTUcampus.jpg              # Campus map image for location selection
├── pin.png                    # Pin icon for marking locations on map
├── pyproject.toml             # Project configuration (UV)
├── uv.lock                    # Locked dependencies (UV)
├── README.md                  # This file
└── .python-version            # Python version specification
```

## Data Format

### canteens.xlsx Structure

The Excel file contains the following columns:
- **Canteen**: Name of the canteen location
- **Stall**: Name of the individual food stall
- **Location**: Coordinates in format "x,y"
- **Price**: Price in SGD (Singapore Dollars)
- **Keywords**: Comma-separated food types/attributes

**Example Row:**
| Canteen | Stall | Location | Price | Keywords |
|---------|-------|----------|-------|----------|
| Food Court 13 | ABC Western | 439,428 | 7.0 | Western, Fries, Burgers, Halal |

## Key Functions

### `load_stall_keywords(data_location)`
Loads and organizes stall keyword data from Excel file.

**Returns:** Dictionary with structure `{canteen: {stall: keywords_string}}`

### `load_stall_prices(data_location)`
Loads and organizes stall price data from Excel file.

**Returns:** Dictionary with structure `{canteen: {stall: price}}`

### `load_canteen_location(data_location)`
Loads and organizes canteen location data from Excel file.

**Returns:** Dictionary with structure `{canteen: [x, y]}`

### `search_by_keyword(keywords)`
Search for stalls matching given keywords.

**Parameters:** keywords dictionary from `load_stall_keywords()`
**Returns:** Dictionary of matching stalls organized by canteen

### `search_by_price(keywords, prices)`
Search for stalls by keywords and maximum price.

**Parameters:** 
- keywords dictionary from `load_stall_keywords()`
- prices dictionary from `load_stall_prices()`

**Returns:** Dictionary of matching stalls with prices

### `search_nearest_canteens(user_locations, k)`
Find k-nearest canteens to the midpoint of two user locations.

**Parameters:**
- user_locations: List of two tuples [(x1, y1), (x2, y2)]
- k: Number of nearest canteens to find (default: 1)

**Returns:** List of tuples [(canteen_name, distance), ...]

### `get_user_locations_interface()`
Interactive map interface to select two user locations on campus.

**Returns:** Tuple of two location tuples ((x1, y1), (x2, y2))

## Troubleshooting

### Issue: "No module named 'arcade'" or missing dependencies

**Solution:** Make sure you've installed dependencies:
```bash
# Using UV:
uv sync

# Or using pip:
pip install -r requirements.txt
```

### Issue: "Location-based Search failed - RuntimeError: No window is active"

**Solution:** This is a known limitation of the arcade library. The map interface can only be used once per program session. To use it again:
1. Exit the program (option 5)
2. Restart the application
3. Select option 4 again

### Issue: Keyword search returns no results

**Solution:** 
- Check spelling (keywords are case-insensitive but must match available keywords)
- Use keywords from the available list (see "Available Keywords" in Usage Guide)
- Try searching for partial words (e.g., "chin" will match "Chinese")
- Search for multiple keywords separated by commas for more flexible results

### Issue: Import errors when running with standard Python

**Solution:** Make sure your virtual environment is activated:
```bash
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

Then run:
```bash
python assignment.py
```

## System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.14 or higher
- **RAM**: Minimum 500MB (2GB+ recommended)
- **Display**: 1024x768 or higher (for interactive map)
- **Dependencies**: Automatically installed via UV or pip

## Performance Notes

- **First run**: May take 30-60 seconds as dependencies are loaded and compiled
- **Subsequent runs**: Much faster as libraries are cached
- **Map interface**: Uses Arcade/Pyglet for fast 2D rendering
- **Data processing**: Uses Pandas for efficient data manipulation

## Known Limitations

1. **Arcade Map Interface (One-time Use)**
   - The map selection interface can only be used once per program session
   - This is a limitation of the Arcade/Pyglet library's event loop
   - Workaround: Exit and restart the program to use the map again

2. **Distance Calculation**
   - Uses Euclidean distance (straight-line distance)
   - Does not account for actual walking paths or road networks
   - Calculates from the midpoint between two users to each canteen

3. **Coordinate System**
   - Uses pixel coordinates from the campus map image
   - Not actual GPS or geographic coordinates
   - Scaling: Map image is scaled to 90% of original size for display

## Future Enhancements

Potential improvements for future versions:
- [ ] Add favorites/bookmarks feature
- [ ] Implement actual GPS integration
- [ ] Add stall ratings and reviews
- [ ] Include opening hours and availability
- [ ] Support for dietary restrictions filtering
- [ ] Mobile app version
- [ ] Web-based interface
- [ ] Real-time crowding information
- [ ] Integration with campus shuttle bus schedules

## Development Notes

### Architecture

The application follows a modular design:
- **Data Loading**: `load_*()` functions handle Excel file parsing
- **Search Functions**: `search_*()` functions implement different search strategies
- **UI**: `MapWindow` class provides interactive map interface using Arcade
- **Menu**: `main()` function handles CLI menu loop

### Code Quality

- Modular functions promote code reusability
- Type hints and docstrings for clarity
- Error handling for invalid user inputs
- Efficient data structures (dictionaries for O(1) lookups)

### Testing

To test individual functions:

```bash
uv run python -c "
from assignment import search_by_keyword, load_stall_keywords
keywords = load_stall_keywords()
results = search_by_keyword(keywords)
"
```

## Credits

- **Assignment**: RE1016 - Data Structures & Algorithms (NTU)
- **Framework**: Arcade (arcade-py.org)
- **Data**: NTU Campus Canteen Information

## License

This project is an educational assignment for Nanyang Technological University.

## Contact & Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the Usage Guide for detailed feature explanations
3. Verify that all dependencies are correctly installed

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Status**: Complete (All features working)

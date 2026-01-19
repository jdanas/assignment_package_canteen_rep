import arcade
from PIL import Image
import pandas as pd
import math


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data["Canteen"].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data["Stall"].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index("Stall")["Keywords"].to_dict()
    stall_canteen_intermediate = copy.set_index("Stall")["Canteen"].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data["Canteen"].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data["Stall"].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index("Stall")["Price"].to_dict()
    stall_canteen_intermediate = copy.set_index("Stall")["Canteen"].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data["Canteen"].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index("Canteen")["Location"].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [
            int(canteen_locations_intermediate[canteen].split(",")[0]),
            int(canteen_locations_intermediate[canteen].split(",")[1]),
        ]

    return canteen_locations


# Arcade window class for map interface
class MapWindow(arcade.Window):
    def __init__(self, image_location, pin_location, screen_title):
        # get image dimensions
        image = Image.open(image_location)
        self.image_width_original, self.image_height_original = image.size
        self.scaled_width = int(self.image_width_original * 0.9)
        self.scaled_height = int(self.image_height_original * 0.9)

        super().__init__(self.scaled_width, self.scaled_height, screen_title)

        self.image_location = image_location
        self.pin_location = pin_location
        self.background = None
        self.pin = None
        self.clicked_x = None
        self.clicked_y = None
        self.pin_placed = False

    def setup(self):
        # Load the background image
        self.background = arcade.load_texture(self.image_location)
        # Load the pin image
        self.pin = arcade.load_texture(self.pin_location)

    def on_draw(self):
        # Clear the screen
        self.clear()
        # Draw the background image
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.scaled_width, self.scaled_height, self.background
        )
        # Draw the pin if placed
        if self.pin_placed and self.clicked_x is not None:
            arcade.draw_lrwh_rectangle_textured(
                self.clicked_x - 30, self.clicked_y - 30, 60, 60, self.pin
            )

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse click
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.clicked_x = x
            self.clicked_y = y
            self.pin_placed = True
            self.on_draw()
            # Close window after brief delay
            arcade.schedule(lambda dt: self.close(), 0.2)

    def on_close(self):
        # Calculate scaled coordinates
        if self.clicked_x is not None and self.clicked_y is not None:
            # Convert from window coordinates to original image coordinates
            # Note: Arcade uses bottom-left origin, so we need to flip Y
            mouseX_scaled = int(self.clicked_x * 1281 / self.scaled_width)
            mouseY_scaled = int(
                (self.scaled_height - self.clicked_y) * 1550 / self.scaled_height
            )
            self.result = (mouseX_scaled, mouseY_scaled)
        else:
            self.result = (None, None)
        super().on_close()


# get user's location with the use of Arcade
def get_user_location_interface():
    image_location = "NTUcampus.jpg"
    pin_location = "pin.png"
    screen_title = "NTU Map"

    window = MapWindow(image_location, pin_location, screen_title)
    window.setup()
    arcade.run()

    return window.result


# Keyword-based Search Function
def search_by_keyword(keywords):
    """
    Search for stalls that match the given keywords.
    Returns a dictionary of {canteen: {stall: keywords}} for matching stalls.
    """
    keyword_input = input("Enter food keywords (comma-separated): ").strip().lower()
    search_keywords = [kw.strip() for kw in keyword_input.split(",")]

    results = {}
    for canteen, stalls in keywords.items():
        for stall, stall_keywords in stalls.items():
            # Check if any search keyword is in the stall's keywords
            stall_keywords_lower = stall_keywords.lower()
            if any(kw in stall_keywords_lower for kw in search_keywords):
                if canteen not in results:
                    results[canteen] = {}
                results[canteen][stall] = stall_keywords

    if results:
        print("\nSearch Results:")
        for canteen, stalls in results.items():
            print(f"\n{canteen}:")
            for stall, kw in stalls.items():
                print(f"  - {stall}: {kw}")
    else:
        print("\nNo matching stalls found for the given keywords.")

    return results


# Price-based Search Function
def search_by_price(keywords, prices):
    """
    Search for stalls that match keywords and are within the max price.
    Returns a dictionary of {canteen: {stall: (keywords, price)}} for matching stalls.
    """
    keyword_input = input("Enter food keywords (comma-separated): ").strip().lower()
    search_keywords = [kw.strip() for kw in keyword_input.split(",")]

    max_price_input = input("Enter maximum price: ").strip()
    try:
        max_price = float(max_price_input)
    except ValueError:
        print("Invalid price entered. Please enter a number.")
        return {}

    results = {}
    for canteen, stalls in keywords.items():
        for stall, stall_keywords in stalls.items():
            # Check if keywords match
            stall_keywords_lower = stall_keywords.lower()
            if any(kw in stall_keywords_lower for kw in search_keywords):
                # Check if price is within budget
                stall_price = prices.get(canteen, {}).get(stall, float("inf"))
                if stall_price <= max_price:
                    if canteen not in results:
                        results[canteen] = {}
                    results[canteen][stall] = (stall_keywords, stall_price)

    if results:
        print("\nSearch Results (within budget):")
        for canteen, stalls in results.items():
            print(f"\n{canteen}:")
            for stall, (kw, price) in stalls.items():
                print(f"  - {stall}: {kw} | Price: ${price:.2f}")
    else:
        print("\nNo matching stalls found within your budget.")

    return results


# Location-based Search Function
def search_nearest_canteens(user_locations, canteen_locations, k):
    """
    Find k nearest canteens to the midpoint of user locations.
    Returns a list of tuples: [(canteen_name, distance), ...]
    """
    # Calculate midpoint between two users
    userA_x, userA_y = user_locations[0]
    userB_x, userB_y = user_locations[1]

    if userA_x is None or userB_x is None:
        print("Invalid user locations. Please try again.")
        return []

    midpoint_x = (userA_x + userB_x) / 2
    midpoint_y = (userA_y + userB_y) / 2

    print(f"\nMidpoint between users (x, y): ({midpoint_x:.1f}, {midpoint_y:.1f})")

    # Calculate distances from midpoint to each canteen
    distances = []
    for canteen, location in canteen_locations.items():
        canteen_x, canteen_y = location
        # Euclidean distance
        distance = math.sqrt(
            (midpoint_x - canteen_x) ** 2 + (midpoint_y - canteen_y) ** 2
        )
        distances.append((canteen, distance))

    # Sort by distance and get top k
    distances.sort(key=lambda x: x[1])
    nearest = distances[:k]

    print(f"\nTop {k} nearest canteens:")
    for i, (canteen, dist) in enumerate(nearest, 1):
        print(f"{i}. {canteen}: {dist:.2f} units away")

    return nearest


# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("========================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("========================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("2 -- Keyword-based Search")

            # call keyword-based search function
            search_by_keyword(canteen_stall_keywords)
        elif option == 3:
            # price-based search
            print("3 -- Price-based Search")

            # call price-based search function
            search_by_price(canteen_stall_keywords, canteen_stall_prices)
        elif option == 4:
            # location-based search
            print("4 -- Location-based Search")

            # call Arcade function to get two users' locations
            print("Click on the map to select User A's location...")
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)

            print("Click on the map to select User B's location...")
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)

            # Get number of nearest canteens to find
            k_input = input("Enter number of nearest canteens to find: ").strip()
            try:
                k = int(k_input)
            except ValueError:
                print("Invalid number. Using default k=5")
                k = 5

            # call location-based search function
            search_nearest_canteens(
                [userA_location, userB_location], canteen_locations, k
            )
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


if __name__ == "__main__":
    main()

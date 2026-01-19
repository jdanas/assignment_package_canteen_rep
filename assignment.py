import pygame
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
    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Canteen", inplace=True)
    canteen_locations_intermediate = copy.set_index("Canteen")["Location"].to_dict()

    for canteen in canteens:
        canteen_locations[canteen] = [
            int(canteen_locations_intermediate[canteen].split(",")[0]),
            int(canteen_locations_intermediate[canteen].split(",")[1]),
        ]

    return canteen_locations


# Pygame window class for map interface - handles both user locations
class MapWindow:
    def __init__(self, image_location, pin_location, screen_title):
        # Initialize pygame
        pygame.init()

        # Get image dimensions
        image = Image.open(image_location)
        self.image_width_original, self.image_height_original = image.size
        self.scaled_width = int(self.image_width_original * 0.9)
        self.scaled_height = int(self.image_height_original * 0.9)

        # Create window
        self.screen = pygame.display.set_mode((self.scaled_width, self.scaled_height))
        pygame.display.set_caption(screen_title)

        self.image_location = image_location
        self.pin_location = pin_location
        self.background = None
        self.pin = None

        # Track both users
        self.user_locations = []  # List to store both user locations
        self.current_user = 1  # Which user we're getting location for (1 or 2)

        self.userA_location = (None, None)
        self.userB_location = (None, None)

        # Font for instructions
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Running flag
        self.running = True

        # Close delay
        self.close_timer = None

    def setup(self):
        # Load and scale the background image
        background_img = pygame.image.load(self.image_location)
        self.background = pygame.transform.scale(
            background_img, (self.scaled_width, self.scaled_height)
        )

        # Load and scale the pin image
        pin_img = pygame.image.load(self.pin_location)
        self.pin = pygame.transform.scale(pin_img, (60, 60))

    def get_instruction_text(self):
        """Get current instruction text based on state"""
        if self.current_user == 1:
            return "Click to select User A's location"
        elif self.current_user == 2:
            return "Click to select User B's location"
        else:
            return "Both locations selected. Closing..."

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background, (0, 0))

        # Draw all placed pins
        for location in self.user_locations:
            x, y = location
            self.screen.blit(self.pin, (x - 30, y - 30))

        # Get instruction text
        instruction_text = self.get_instruction_text()

        # Render text
        text_surface = self.font.render(instruction_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()

        # Center text at top
        text_rect.centerx = self.scaled_width // 2
        text_rect.top = 30

        # Draw semi-transparent background rectangle for text visibility
        padding = 10
        background_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + 2 * padding,
            text_rect.height + 2 * padding,
        )

        # Create semi-transparent surface
        s = pygame.Surface((background_rect.width, background_rect.height))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        self.screen.blit(s, background_rect.topleft)

        # Draw instruction text on top
        self.screen.blit(text_surface, text_rect)

        # Update display
        pygame.display.flip()

    def handle_mouse_click(self, pos):
        """Handle mouse click event"""
        x, y = pos

        if self.current_user <= 2:
            # Store the clicked location
            self.user_locations.append((x, y))

            # Convert to scaled coordinates
            mouseX_scaled = int(x * 1281 / self.scaled_width)
            mouseY_scaled = int((self.scaled_height - y) * 1550 / self.scaled_height)

            if self.current_user == 1:
                self.userA_location = (mouseX_scaled, mouseY_scaled)
                print(f"User A's location (x, y): {self.userA_location}")
                self.current_user = 2
            elif self.current_user == 2:
                self.userB_location = (mouseX_scaled, mouseY_scaled)
                print(f"User B's location (x, y): {self.userB_location}")
                self.current_user = 3
                # Set close timer (0.5 seconds)
                self.close_timer = pygame.time.get_ticks() + 500

    def run(self):
        """Main event loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_mouse_click(event.pos)

            # Draw everything
            self.draw()

            # Check close timer
            if self.close_timer is not None:
                if pygame.time.get_ticks() >= self.close_timer:
                    self.running = False

            # Control frame rate
            self.clock.tick(60)

        # Cleanup
        pygame.quit()


# get both user locations with pygame interface
def get_user_locations_interface():
    image_location = "NTUcampus.jpg"
    pin_location = "pin.png"
    screen_title = "NTU Map - Select User Locations"

    window = MapWindow(image_location, pin_location, screen_title)
    window.setup()
    window.run()

    return window.userA_location, window.userB_location


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
def search_nearest_canteens(user_locations, k):
    """
    Find k nearest canteens to the midpoint of user locations.
    Returns a list of tuples: [(canteen_name, distance), ...]
    """
    # Load canteen locations from data file
    canteen_locations = load_canteen_location("canteens.xlsx")

    # Calculate midpoint between two users
    userA_x, userA_y = user_locations[0]
    userB_x, userB_y = user_locations[1]

    if userA_x is None or userB_x is None:
        print("Invalid user locations. Please try again.")
        return []

    # Validate k value - must be positive
    if k <= 0:
        print("Warning: k must be positive. Default k = 1 is set.")
        k = 1

    midpoint_x = (userA_x + userB_x) / 2
    midpoint_y = (userA_y + userB_y) / 2

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

    # Print results with proper singular/plural handling
    if k == 1:
        print("1 Nearest Canteen found:")
    else:
        print(f"{k} Nearest Canteens found:")

    # Format: "Canteen Name – 156m" (en-dash, integer meters, no numbering)
    for canteen, dist in nearest:
        print(f"{canteen} – {dist:.0f}m")

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
        try:
            option = int(input("Enter option [1-5]: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if option < 1 or option > 5:
            print("Invalid option. Please enter a number between 1 and 5.")
            continue

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

            # call Arcade function to get both users' locations
            print("Click on the map to select both user locations...")
            userA_location, userB_location = get_user_locations_interface()

            # Get number of nearest canteens to find
            k_input = input("Enter number of nearest canteens to find: ").strip()
            try:
                k = int(k_input)
            except ValueError:
                print("Invalid number. Using default k=1")
                k = 1

            # Validate k is positive
            if k <= 0:
                print("Warning: k must be positive. Default k = 1 is set.")
                k = 1

            # call location-based search function
            search_nearest_canteens([userA_location, userB_location], k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


if __name__ == "__main__":
    main()

from picovector import ANTIALIAS_FAST,ANTIALIAS_BEST, PicoVector, Polygon, Transform
from presto import Presto
import network
import urequests
import time
import math
import random

# Initialize Presto and display
presto = Presto(ambient_light=True)
display = presto.display
WIDTH, HEIGHT = display.get_bounds()

# Colors
COLORS = [
    display.create_pen(28, 181, 202),  # Blue
    display.create_pen(245, 165, 4),  # Orange
    display.create_pen(230, 60, 45),  # Red
    display.create_pen(250, 125, 180),  # Pink
    display.create_pen(118, 95, 210),  # Purple
    display.create_pen(9, 185, 120),  # Green
]

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

# Initialize PicoVector
vector = PicoVector(display)
vector.set_antialiasing(ANTIALIAS_BEST)

# Font settings
FONT = "cherry-hq.af"
vector.set_font(FONT, 72)
vector.set_font_letter_spacing(100)
vector.set_font_word_spacing(100)

# Transform for text rendering
text_transform = Transform()

# Wi-Fi credentials (stored in secrets.py)
from secrets import WIFI_SSID, WIFI_PASSWORD

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected:", wlan.ifconfig())

# Fetch a random dad joke
def fetch_joke():
    headers = {
        "Accept": "application/json",
        "User-Agent": "HeyPrestoDadJokeDisplayer (https://github.com/your-repo)"
    }
    try:
        print("Fetching joke from API...")
        response = urequests.get("https://icanhazdadjoke.com/", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("joke", "No joke found!")
        else:
            return "Couldn't fetch a joke!"
    except Exception as e:
        print(f"Error fetching joke: {e}")
        return "Error fetching joke."

# Adjust font size dynamically
def adjust_font_size(joke):
    font_size = 72
    max_width = WIDTH - 40
    max_height = HEIGHT - 40

    while font_size > 20:
        vector.set_font_size(font_size)
        _, _, text_width, text_height = vector.measure_text(joke)
        if text_width <= max_width and text_height <= max_height:
            return font_size
        font_size -= 2

    return 20  # Fallback to minimum font size

# Animated Backgrounds

def falling_confetti():
    # Create confetti pieces with random sizes and properties
    confetti = []
    positions = []
    speeds = []
    rotations = []
    sizes = []

    for _ in range(30):  # Number of confetti pieces
        piece = Polygon()

        # Random rectangle size
        width = random.randint(5, 15)
        height = random.randint(10, 20)
        piece.rectangle(0, 0, width, height)

        # Assign random starting positions and speeds
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        speed = random.uniform(2, 6)  # Falling speed
        rotation = random.uniform(0, 360)  # Initial rotation
        size = random.uniform(0.8, 1.5)  # Scale size

        confetti.append(piece)
        positions.append([x, y])
        speeds.append(speed)
        rotations.append(rotation)
        sizes.append(size)

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()

        for i, (x, y) in enumerate(positions):
            # Update position and rotation
            positions[i][1] += speeds[i]  # Falling speed
            positions[i][0] += math.sin(tick / 20) * 2  # Oscillation effect
            rotations[i] = (rotations[i] + speeds[i]) % 360  # Continuous rotation

            # Reset confetti when it falls out of bounds
            if y > HEIGHT:
                positions[i][1] = -20  # Reset to just above the screen
                positions[i][0] = random.randint(0, WIDTH)  # Random horizontal position
                rotations[i] = random.uniform(0, 360)  # Reset rotation

            # Set random color
            display.set_pen(COLORS[i % len(COLORS)])

            # Apply transformations
            t = Transform()
            t.translate(positions[i][0], positions[i][1])
            t.rotate(rotations[i], (0, 0))
            t.scale(sizes[i], sizes[i])
            vector.set_transform(t)

            # Draw the rectangle
            vector.draw(confetti[i])

    return draw



def rising_balloons():
    # Number of balloons
    balloons = []
    knots = []
    positions = []
    speeds = []
    sizes = []

    for _ in range(10):
        # Create the balloon body (circle)
        balloon = Polygon()
        radius = random.randint(20, 40)
        balloon.circle(0, 0, radius)

        # Create the knot (small rectangle)
        knot = Polygon()
        knot_width = radius // 4
        knot_height = radius // 6
        knot.rectangle(-knot_width // 2, 0, knot_width, knot_height)

        # Store position and motion properties
        x = random.randint(0, WIDTH)
        y = random.randint(-HEIGHT, 0)
        speed = random.uniform(1, 3)  # Rising speed

        balloons.append(balloon)
        knots.append(knot)
        positions.append([x, y])
        speeds.append(speed)
        sizes.append(radius)

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()

        for i, (x, y) in enumerate(positions):
            positions[i][1] -= speeds[i]  # Rising speed
            positions[i][0] += math.sin(tick / 30) * 2  # Horizontal drift

            # Reset balloon if it goes off-screen
            if y < -50 - sizes[i]:  # Ensure the entire balloon is off-screen
                positions[i][1] = HEIGHT
                positions[i][0] = random.randint(0, WIDTH)

            # Set random color for the balloon
            color = COLORS[i % len(COLORS)]
            display.set_pen(color)

            # Draw the balloon body
            t = Transform()
            t.translate(x, y)
            vector.set_transform(t)
            vector.draw(balloons[i])

            # Draw the knot in the same color as the balloon
            t = Transform()
            t.translate(x, y + sizes[i])  # Position at the bottom of the balloon
            vector.set_transform(t)
            vector.draw(knots[i])

            # Draw the tether string
            string = Polygon()
            string.rectangle(-1, 0, 2, 40)  # Narrow rectangle for string
            display.set_pen(WHITE)
            t = Transform()
            t.translate(x, y + sizes[i] + 10)  # Slightly below the knot
            vector.set_transform(t)
            vector.draw(string)

    return draw



def scrolling_clouds():
    clouds = []
    positions = []
    speeds = []
    colors = []

    for _ in range(5):  # Number of clouds
        # Create a cloud as a list of circles
        cloud = []
        num_puffs = random.randint(4, 6)  # Random number of circles per cloud
        base_size = random.randint(20, 40)  # Base size for puffs
        for _ in range(num_puffs):
            offset_x = random.randint(-base_size, base_size)  # Horizontal offset
            offset_y = random.randint(-base_size // 2, base_size // 2)  # Vertical offset
            size = random.randint(base_size // 2, base_size)  # Random size for each puff
            cloud.append((offset_x, offset_y, size))  # Store circle properties

        # Assign random starting positions, speeds, and colors
        x = random.randint(-WIDTH, WIDTH)  # Start off-screen for scrolling
        y = random.randint(HEIGHT // 4, 3 * HEIGHT // 4)  # Random vertical position
        speed = random.uniform(0.5, 2)  # Slow scrolling speed
        color = COLORS[random.randint(0, len(COLORS) - 1)]  # Random solid color

        clouds.append(cloud)
        positions.append([x, y])
        speeds.append(speed)
        colors.append(color)

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()

        for i, (x, y) in enumerate(positions):
            # Update position
            positions[i][0] -= speeds[i]  # Scroll leftward
            if x < -WIDTH:  # Reset cloud when it goes off-screen
                positions[i][0] = WIDTH + 50  # Start off the right edge
                positions[i][1] = random.randint(HEIGHT // 4, 3 * HEIGHT // 4)  # Random vertical position

            # Set cloud color
            display.set_pen(colors[i])

            # Draw each circle in the cloud
            for offset_x, offset_y, size in clouds[i]:
                t = Transform()
                t.translate(positions[i][0] + offset_x, positions[i][1] + offset_y)
                vector.set_transform(t)
                puff = Polygon()
                puff.circle(0, 0, size)
                vector.draw(puff)

    return draw



def spinning_stars():
    stars = [Polygon() for _ in range(5)]
    for star in stars:
        star.star(0, 0, 5, 20, 70)

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()
        for i, star in enumerate(stars):
            angle = (tick + i * 20) % 360
            t = Transform()
            t.translate(WIDTH // 2, HEIGHT // 2)
            t.rotate(angle, (0, 0))
            t.scale(1 + i / 10,  1 + i / 10)
            vector.set_transform(t)
            display.set_pen(COLORS[i % len(COLORS)])
            vector.draw(star)

    return draw

def pulsing_blobs():
    blobs = []
    positions = []
    base_scales = []
    colors = []

    for _ in range(5):  # Number of blobs
        # Generate random points for an organic blob shape
        num_points = random.randint(6, 10)  # Number of "arms" for the blob
        radius = random.randint(20, 40)  # Base radius
        points = []
        for angle in range(0, 360, 360 // num_points):
            rad = math.radians(angle)
            r = radius + random.randint(-10, 10)  # Add randomness to radius
            x = int(r * math.cos(rad))
            y = int(r * math.sin(rad))
            points.append((x, y))

        # Create the blob using the random points
        blob = Polygon()
        blob.path(*points)  # Pass the points to define the blob's path

        # Random starting positions and scales
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        base_scale = random.uniform(0.8, 1.2)

        blobs.append(blob)
        positions.append([x, y])
        base_scales.append(base_scale)
        colors.append(COLORS[random.randint(0, len(COLORS) - 1)])  # Random initial color

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()

        for i, (x, y) in enumerate(positions):
            # Smooth pulsing effect
            scale = base_scales[i] + 0.5 * math.sin((tick + i * 50) / 30)

            # Cycle through colors
            color_index = (tick // 20 + i) % len(COLORS)
            display.set_pen(COLORS[color_index])

            # Apply transformations
            t = Transform()
            t.translate(x, y)
            t.scale(scale, scale)
            vector.set_transform(t)

            # Draw the blob
            vector.draw(blobs[i])

    return draw

def space_travel_stars():
    stars = []

    # Generate stars with random starting angles, speeds, and colors
    for _ in range(50):  # Number of stars
        star = Polygon()
        star.circle(0, 0, 2)  # Small circle to represent the star

        # Assign random properties
        angle = random.uniform(0, 360)  # Direction in degrees
        speed = random.uniform(2, 6)  # Speed of outward movement
        size = random.uniform(1, 2)  # Initial size
        color = COLORS[random.randint(0, len(COLORS) - 1)]  # Random color
        x = WIDTH // 2
        y = HEIGHT // 2

        stars.append({
            "star": star,
            "angle": angle,
            "speed": speed,
            "size": size,
            "color": color,
            "pos": [x, y]
        })

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()

        for star_data in stars:
            star = star_data["star"]
            angle = star_data["angle"]
            speed = star_data["speed"]
            size = star_data["size"]
            color = star_data["color"]
            pos = star_data["pos"]

            # Calculate movement based on angle
            rad = math.radians(angle)
            pos[0] += speed * math.cos(rad)  # Update X position
            pos[1] += speed * math.sin(rad)  # Update Y position

            # Scale the star as it moves outward
            size += 0.05
            star_data["size"] = size

            # Reset the star when it moves off-screen
            if pos[0] < -10 or pos[0] > WIDTH + 10 or pos[1] < -10 or pos[1] > HEIGHT + 10:
                pos[0] = WIDTH // 2
                pos[1] = HEIGHT // 2
                star_data["size"] = random.uniform(1, 2)  # Reset size
                star_data["angle"] = random.uniform(0, 360)  # New random direction
                star_data["speed"] = random.uniform(2, 6)  # New random speed
                star_data["color"] = COLORS[random.randint(0, len(COLORS) - 1)]  # New random color

            # Set star color
            display.set_pen(color)

            # Apply transformations for scaling and positioning
            t = Transform()
            t.translate(pos[0], pos[1])
            t.scale(size, size)
            vector.set_transform(t)

            # Draw the star
            vector.draw(star)

    return draw



# Display joke with animation
def display_with_animation(joke, draw_animation):
    tick = 0
    start_time = time.time()

    # Split the joke into setup and punchline
    split_point = joke.find("?") + 1 if "?" in joke else joke.find(".") + 1
    if split_point == 0:  # If neither "?" nor "." found, show the joke as-is
        setup = joke
        punchline = ""
    else:
        setup = joke[:split_point].strip()
        punchline = joke[split_point:].strip()

    # Determine the maximum font size that fits both lines
    combined_text = setup + "\n" + punchline  # Combine for measurement
    font_size = adjust_font_size(combined_text)

    while time.time() - start_time < 60:  # Display for 60 seconds
        # Clear the screen and draw animation
        display.set_pen(BLACK)
        display.clear()
        draw_animation(tick)

        # Set the determined font size
        vector.set_font_size(font_size)

        # Draw setup text
        display.set_pen(WHITE)
        text_transform.reset()
        text_transform.translate(WIDTH // 2, HEIGHT // 3)  # Top third of the screen
        vector.set_transform(text_transform)
        vector.text(setup, -WIDTH // 2 + 20, -font_size // 2, max_width=WIDTH - 40)

        # Draw punchline text
        text_transform.reset()
        text_transform.translate(WIDTH // 2, 2 * HEIGHT // 3)  # Bottom third of the screen
        vector.set_transform(text_transform)
        vector.text(punchline, -WIDTH // 2 + 20, -font_size // 2, max_width=WIDTH - 40)

        # Refresh the display
        presto.update()
        tick += 1


# Main program
def main():
    connect_to_wifi()
    print("Wi-Fi connected. Starting animation loop...")
    
    # Ensure all animations are included
    animations = [
        falling_confetti(),
        rising_balloons(),
        scrolling_clouds(),
        spinning_stars(),
        pulsing_blobs(),
        space_travel_stars()
    ]
    animation_index = 0

    while True:
        print(f"Fetching joke for animation {animation_index}...")
        joke = fetch_joke()
        print(f"Joke fetched: {joke}")
        
        try:
            print(f"Running animation {animation_index}...")
            display_with_animation(joke, animations[animation_index])
            print(f"Animation {animation_index} completed.")
            
            # Rotate to the next animation
            animation_index = (animation_index + 1) % len(animations)
        except Exception as e:
            print(f"Error during animation: {e}")


main()


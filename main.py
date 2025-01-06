#Dedicated to Jenius

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
        "User-Agent": "HeyPrestoDadJokeDisplayer (https://github.com/mrglennjones/prestohoho)"
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
    balloons = [Polygon() for _ in range(10)]
    positions = [[random.randint(0, WIDTH), random.randint(-HEIGHT, 0)] for _ in balloons]
    speeds = [random.randint(1, 3) for _ in balloons]

    for balloon in balloons:
        balloon.circle(0, 0, random.randint(10, 50))

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()
        for i, (x, y) in enumerate(positions):
            positions[i][1] -= speeds[i]
            if y < -20:
                positions[i][1] = HEIGHT  # Reset to the bottom
                positions[i][0] = random.randint(0, WIDTH)
            display.set_pen(COLORS[i % len(COLORS)])
            t = Transform()
            t.translate(x, y)
            vector.set_transform(t)
            vector.draw(balloons[i])

    return draw

def scrolling_clouds():
    clouds = [Polygon() for _ in range(5)]
    positions = [random.randint(-100, WIDTH) for _ in clouds]

    for cloud in clouds:
        cloud.circle(0, 0, random.randint(10, 50))

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()
        for i, x in enumerate(positions):
            positions[i] -= 2
            if x < -40:
                positions[i] = WIDTH + 40  # Reset to the right
            display.set_pen(COLORS[i % len(COLORS)])
            t = Transform()
            t.translate(x, HEIGHT // 4 + i * 40)
            vector.set_transform(t)
            vector.draw(clouds[i])

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
    blobs = [Polygon() for _ in range(5)]
    for blob in blobs:
        blob.circle(0, random.randint(0, 70), random.randint(0, 100))

    def draw(tick):
        display.set_pen(BLACK)
        display.clear()
        for i, blob in enumerate(blobs):
            scale = 1 + 0.5 * math.sin((tick + i * 50) / 100)
            t = Transform()
            t.translate(WIDTH // 2, HEIGHT // 2)
            t.scale(scale, scale)
            t.translate(-50 + i * 40, -50 + i * 40)
            display.set_pen(COLORS[i % len(COLORS)])
            vector.set_transform(t)
            vector.draw(blob)

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
        pulsing_blobs()
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


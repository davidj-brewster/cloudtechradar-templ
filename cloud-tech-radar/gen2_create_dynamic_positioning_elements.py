import random
from math import cos, sin, radians, sqrt, atan2
from PIL import ImageFont, ImageDraw, Image
import os
import requests
import json

# Constants and static variables
DEBUG = True  # Set to True to enable debug logging
INITIAL_CANVAS_SIZE = 1600
MEDIUM_FONT_SIZE = 16
SMALL_FONT_SIZE = 12
LARGE_FONT_SIZE = 40
REPULSION_CONSTANT = 5000
ATTRACTION_CONSTANT = 0.1
DAMPING = 0.85
LEEWAY = 0.1  # 10% leeway

# Load fonts
large_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", LARGE_FONT_SIZE)
medium_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", MEDIUM_FONT_SIZE)
small_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", SMALL_FONT_SIZE)

def log_debug(message):
    """Print debug messages if debugging is enabled."""
    if DEBUG:
        print(f"DEBUG: {message}")

# Load product data
with open('product_definitions.json') as f:
    product_definitions = json.load(f)
with open('tech_radar_classifications.json') as f:
    classifications = json.load(f)
with open('tech_radar_product_categories.json') as f:
    product_categories = json.load(f)

# Debug: Print the structure of product_categories
log_debug(f"Product Categories: {product_categories}")

# Reverse the product categories to map the full names to the shorter keys
category_map = {value: key for key, value in product_categories.items()}

# Generate tech radar data structure
tech_radar = {
    "quadrants": [{"id": key, "name": value} for key, value in product_categories.items()],
    "rings": [
        {"id": "adopt", "name": "Adopt"},
        {"id": "evaluation", "name": "Evaluate"},
        {"id": "hold", "name": "Hold"},
        {"id": "retire", "name": "Retire"}
    ],
    "entries": []
}

# Mapping product names to their respective rings
product_to_ring = {}
for ring, products in classifications.items():
    for product in products:
        product_to_ring[product] = ring

# Populate tech radar entries
for product_name, product in product_definitions.items():
    category_name = product.get("category")
    quadrant = category_map.get(category_name, None)
    if quadrant:
        tech_radar['entries'].append({
            "id": product_name,
            "title": product["name"],
            "quadrant": quadrant,
            "timeline": [{"ring": product_to_ring.get(product_name, "hold")}],
            "description": product["description"],
            "image_url": product.get("image_url"),
            "file_path": product.get("file_path")  # Added file_path here
        })

# Variables for quadrant and ring calculations
quadrant_angle_step = 360 / len(tech_radar['quadrants'])

# Adjust ring radii to ensure the middle ring is larger
ring_radius = [INITIAL_CANVAS_SIZE // 8, INITIAL_CANVAS_SIZE // 4, INITIAL_CANVAS_SIZE // 2, 3 * INITIAL_CANVAS_SIZE // 4]
center_x = center_y = INITIAL_CANVAS_SIZE // 2

# Function to calculate text size
def calculate_text_size(entry, font):
    """Calculate the width and height of the text for the given entry."""
    text = entry['title']
    dummy_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    text_size = draw.textsize(text, font=font)
    return text_size

# Function to adjust sizes if too crowded
def adjust_sizes(entries, center_x, center_y, ring_radius, quadrants, canvas_size):
    """Adjust sizes and canvas if nodes are too crowded."""
    max_attempts = 10
    global medium_font, small_font, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE
    
    for attempt in range(max_attempts):
        placed_entries = initial_placement(entries, quadrants, ring_radius, center_x, center_y, medium_font)
        if not is_crowded(placed_entries):
            return placed_entries, medium_font, small_font, ring_radius, center_x, center_y, canvas_size
        
        # Reduce font sizes and increase ring radius
        if MEDIUM_FONT_SIZE > 12:
            MEDIUM_FONT_SIZE -= 1
            medium_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", MEDIUM_FONT_SIZE)
        if SMALL_FONT_SIZE > 7:
            SMALL_FONT_SIZE -= 1
            small_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", SMALL_FONT_SIZE)
        
        ring_radius = [r * 1.1 for r in ring_radius]
        canvas_size = int(canvas_size * 1.1)
        center_x = center_y = canvas_size // 2

        # Ensure the furthest ring radius does not exceed half the canvas size
        max_ring_radius = canvas_size // 2
        if ring_radius[-1] > max_ring_radius:
            ring_radius = [r * (max_ring_radius / ring_radius[-1]) for r in ring_radius]
    
    log_debug("Maximum adjustment attempts reached. Using the last adjusted sizes.")
    return placed_entries, medium_font, small_font, ring_radius, center_x, center_y, canvas_size

# Function to check if nodes are crowded
def is_crowded(placed_entries):
    """Check if nodes are crowded based on their sizes."""
    for i, (xi, yi, wi, hi, _, _, _) in enumerate(placed_entries):
        for j, (xj, yj, wj, hj, _, _, _) in enumerate(placed_entries):
            if i != j:
                distance = sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
                min_distance = (wi + wj) / 2 + (hi + hj) / 2
                if distance < min_distance:
                    return True
    return False

# Function for initial placement of entries
def initial_placement(entries, quadrants, ring_radius, center_x, center_y, font):
    """Place nodes initially based on their quadrants and rings."""
    placed_entries = []
    for entry in entries:
        try:
            quadrant_index = next((i for i, q in enumerate(quadrants) if q['id'] == entry['quadrant']), None)
            if quadrant_index is None:
                raise ValueError(f"Quadrant {entry['quadrant']} not found for entry {entry['title']}")
            
            product_name = entry["title"]
            ring_name = product_to_ring.get(product_name, 'hold')
            ring_index = next((i for i, r in enumerate(tech_radar['rings']) if r['id'] == ring_name), None)
            if ring_index is None:
                raise ValueError(f"Ring {ring_name} not found for entry {product_name}")

            angle_start = quadrant_index * quadrant_angle_step
            angle_end = angle_start + quadrant_angle_step
            angle = (angle_start + angle_end) / 2

            if ring_name == "adopt":
                # Special rule for "adopt": place anywhere within the innermost ring
                radius = random.uniform(0, ring_radius[0] - 5)
                angle = random.uniform(0, 360)
            elif ring_index == 0:
                radius = random.uniform(0, ring_radius[0] - 5)
            else:
                radius = ring_radius[ring_index] - 5

            angle += random.uniform(-quadrant_angle_step / 10, quadrant_angle_step / 10)
            x = center_x + radius * cos(radians(angle))
            y = center_y + radius * sin(radians(angle))
            text_width, text_height = calculate_text_size(entry, font)
            placed_entries.append([x, y, text_width, text_height, quadrant_index, ring_index, entry])
            log_debug(f"Placed {product_name} at x={x}, y={y}, quadrant_index={quadrant_index}, ring_index={ring_index}")
        except ValueError as e:
            log_debug(f"Error in initial placement: {e}")
    
    return placed_entries

# Function to adjust positions using force-directed algorithm
def adjust_positions(placed_entries, quadrants, rings, center_x, center_y, ring_radius, iterations=50):
    """Adjust node positions using a force-directed algorithm."""
    for _ in range(iterations):
        for i in range(len(placed_entries)):
            xi, yi, wi, hi, quadrant_index_i, ring_index_i, entry_i = placed_entries[i]
            fx = 0
            fy = 0
            for j in range(len(placed_entries)):
                if i != j:
                    xj, yj, wj, hj, quadrant_index_j, ring_index_j, entry_j = placed_entries[j]
                    dx = xi - xj
                    dy = yi - yj
                    distance = sqrt(dx * dx + dy * dy) + 0.1  # Add a small constant to avoid division by zero
                    min_distance = (wi + wj) / 2 + (hi + hj) / 2  # Minimum distance based on node sizes
                    if distance < min_distance:
                        repulsion = REPULSION_CONSTANT / (distance * distance)
                        fx += repulsion * (dx / distance)
                        fy += repulsion * (dy / distance)

            # Attraction to original position within constraints
            original_x, original_y = initial_placement_position(entry_i, quadrants, rings, center_x, center_y, ring_radius)
            dx = original_x - xi
            dy = original_y - yi
            distance = sqrt(dx * dx + dy * dy)
            attraction = ATTRACTION_CONSTANT * distance
            fx += attraction * (dx / distance)
            fy += attraction * (dy / distance)

            # Apply forces to the position
            xi += fx * DAMPING
            yi += fy * DAMPING

            # Constrain to the quadrant and ring with leeway
            if entry_i['timeline'][0]['ring'] != "adopt":
                xi, yi = constrain_to_quadrant_and_ring_with_leeway(xi, yi, quadrant_index_i, ring_index_i, center_x, center_y, ring_radius, quadrant_angle_step, LEEWAY)

            placed_entries[i][0] = xi
            placed_entries[i][1] = yi

    return placed_entries

# Constrain position to quadrant and ring with leeway
def constrain_to_quadrant_and_ring_with_leeway(x, y, quadrant_index, ring_index, center_x, center_y, ring_radius, quadrant_angle_step, leeway):
    """Constrain node positions to their quadrants and rings with some leeway."""
    angle_start = quadrant_index * quadrant_angle_step
    angle_end = angle_start + quadrant_angle_step
    min_radius = 0 if ring_index == 0 else ring_radius[ring_index - 1] * (1 - leeway)
    max_radius = ring_radius[ring_index] * (1 + leeway)

    dx = x - center_x
    dy = y - center_y
    distance = sqrt(dx * dx + dy * dy)
    angle = (angle_start + angle_end) / 2

    # Constrain distance
    if distance < min_radius:
        distance = min_radius
    if distance > max_radius:
        distance = max_radius

    # Constrain angle
    current_angle = atan2(dy, dx)
    angle_leeway = quadrant_angle_step * leeway / 2
    min_angle = radians(angle_start - angle_leeway)
    max_angle = radians(angle_end + angle_leeway)

    if current_angle < min_angle:
        current_angle = min_angle
    if current_angle > max_angle:
        current_angle = max_angle

    # Convert constrained polar coordinates back to Cartesian coordinates
    x = center_x + distance * cos(current_angle)
    y = center_y + distance * sin(current_angle)
    
    log_debug(f"Constrained position to quadrant and ring with leeway: x={x}, y={y}, quadrant_index={quadrant_index}, ring_index={ring_index}")
    return x, y

# Get initial placement position
def initial_placement_position(entry, quadrants, rings, center_x, center_y, ring_radius):
    """Calculate the initial placement position for a given entry."""
    quadrant_index = next((i for i, q in enumerate(quadrants) if q['id'] == entry['quadrant']), None)
    product_name = entry["title"]
    ring_name = product_to_ring.get(product_name, 'hold')
    ring_index = next((i for i, r in enumerate(rings) if r['id'] == ring_name), None)

    angle_start = quadrant_index * quadrant_angle_step
    angle_end = angle_start + quadrant_angle_step
    angle = (angle_start + angle_end) / 2

    if ring_name == "adopt":
        # Special rule for "adopt": place anywhere within the innermost ring
        radius = random.uniform(0, ring_radius[0] - 5)
        angle = random.uniform(0, 360)
    elif ring_index == 0:
        radius = random.uniform(0, ring_radius[0] - 5)
    else:
        radius = ring_radius[ring_index] - 5

    angle += random.uniform(-quadrant_angle_step / 10, quadrant_angle_step / 10)
    x = center_x + radius * cos(radians(angle))
    y = center_y + radius * sin(radians(angle))
    
    log_debug(f"Initial placement position: x={x}, y={y}, quadrant_index={quadrant_index}, ring_index={ring_index}")
    return x, y

# Main logic
tech_radar_entries = tech_radar['entries']
center_x = center_y = INITIAL_CANVAS_SIZE // 2

initial_positions, medium_font, small_font, ring_radius, center_x, center_y, canvas_size = adjust_sizes(tech_radar_entries, center_x, center_y, ring_radius, tech_radar['quadrants'], INITIAL_CANVAS_SIZE)
adjusted_positions = adjust_positions(initial_positions, tech_radar['quadrants'], tech_radar['rings'], center_x, center_y, ring_radius)

# Create canvas
canvas_size = max(center_x, center_y) * 2
img = Image.new('RGB', (canvas_size, canvas_size), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Function to add images to the canvas
def add_images(entry, draw, img, x, y):
    """Resize and add images to the canvas."""
    try:
        local_img_path = entry["file_path"]  # Use the file_path directly from product_definitions
        if not os.path.exists(local_img_path):
            # Download image if it doesn't exist locally
            image_url = entry.get('image_url')
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200 and 'image' in response.headers['Content-Type']:
                    with open(local_img_path, 'wb') as f:
                        f.write(response.content)
                else:
                    raise Exception(f"Failed to download image for {entry['id']} from {image_url} (status code: {response.status_code}, content type: {response.headers['Content-Type']})")
            else:
                raise Exception(f"No local image or image URL for {entry['id']}")

        img = Image.open(local_img_path)
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        new_height = 50
        new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img_x = x - new_width // 2
        img_y = y - new_height // 2
        img.paste(img, (int(img_x), int(img_y)))
        return int(img_x), int(img_y), new_width, new_height
    except FileNotFoundError:
        log_debug(f"Image file for {entry['id']} not found.")
    except IOError:
        log_debug(f"Error opening image for {entry['id']}.")
    except Exception as e:
        log_debug(f"Error adding image for {entry['id']}: {e}")
    return None, None, None, None

# Place adjusted entries on the image
for x, y, w, h, _, _, entry in adjusted_positions:
    img_x, img_y, img_w, img_h = add_images(entry, draw, img, x, y)
    if img_x is not None:
        draw.text((img_x - img_w / 2 + 1, img_y - img_h - 10), entry['title'], font=medium_font, fill="black", anchor="mm")

# Add category labels
for quadrant in tech_radar['quadrants']:
    angle_start = tech_radar['quadrants'].index(quadrant) * quadrant_angle_step
    angle_end = angle_start + quadrant_angle_step
    angle = (angle_start + angle_end) / 2
    label_x = center_x + ring_radius[-1] * 1.1 * cos(radians(angle))
    label_y = center_y + ring_radius[-1] * 1.1 * sin(radians(angle))
    draw.text((label_x, label_y), quadrant['name'], font=large_font, fill="black", anchor="mm")
    log_debug(f"Added category label for {quadrant['name']} at ({label_x}, {label_y})")

# Draw the rings
for radius in ring_radius:
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline='black')
    log_debug(f"Drew ring with radius {radius}")

# Save image
img.save('tech_radar.png')


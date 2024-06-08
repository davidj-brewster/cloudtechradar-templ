import random
from math import cos, sin, radians, sqrt, atan2
from PIL import ImageFont, ImageDraw, Image
import os
import requests
import json
import yaml

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

def load_data():
    """Load product data from JSON files."""
    with open('product_definitions.json') as f:
        product_definitions = json.load(f)
    with open('tech_radar_classifications.json') as f:
        classifications = json.load(f)
    with open('tech_radar_product_categories.json') as f:
        product_categories = json.load(f)
    return product_definitions, classifications, product_categories

def map_data_to_structure(product_definitions, classifications, product_categories):
    """Map the product data to the tech radar structure."""
    category_map = {
        "Data / ML": "Languages & Frameworks",
        "Storage": "Tools",
        "Compute": "Platforms",
        "DevOps": "Techniques",
        "Observability": "Techniques"
    }

    ring_map = {
        "adopt": {"id": 0, "name": "Adopt", "color": "#93c47d"},
        "evaluation": {"id": 1, "name": "Trial", "color": "#93d2c2"},
        "hold": {"id": 2, "name": "Assess", "color": "#fbdb84"},
        "retire": {"id": 3, "name": "Hold", "color": "#efafa9"}
    }

    tech_radar = {
        "quadrants": [{"id": key, "name": value} for key, value in category_map.items()],
        "rings": [details for ring, details in ring_map.items()],
        "entries": []
    }

    product_to_ring = {}
    for ring, products in classifications.items():
        for product in products:
            product_to_ring[product] = ring

    for product_name, product in product_definitions.items():
        category_name = product.get("category")
        quadrant_id = category_map.get(category_name, None)
        ring_name = product_to_ring.get(product_name, "hold")
        ring_id = ring_map.get(ring_name, {}).get("id", 2)

        if quadrant_id is not None:
            tech_radar['entries'].append({
                "id": product_name,
                "title": product["name"],
                "quadrant": quadrant_id,
                "timeline": [{"ring": ring_name}],
                "description": product["description"],
                "image_url": product.get("image_url"),
                "file_path": product.get("file_path")
            })

    return tech_radar

def calculate_text_size(entry, font):
    """Calculate the width and height of the text for the given entry."""
    text = entry['title']
    dummy_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    text_size = draw.textsize(text, font=font)
    return text_size

def adjust_sizes(entries, center_x, center_y, ring_radius, quadrants, canvas_size):
    """Adjust sizes and canvas if nodes are too crowded."""
    max_attempts = 10
    global medium_font, small_font, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE
    
    for attempt in range(max_attempts):
        placed_entries = initial_placement(entries, quadrants, ring_radius, center_x, center_y, medium_font)
        if not is_crowded(placed_entries):
            return placed_entries, medium_font, small_font, ring_radius, center_x, center_y, canvas_size
        
        if MEDIUM_FONT_SIZE > 12:
            MEDIUM_FONT_SIZE -= 1
            medium_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", MEDIUM_FONT_SIZE)
        if SMALL_FONT_SIZE > 7:
            SMALL_FONT_SIZE -= 1
            small_font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", SMALL_FONT_SIZE)
        
        ring_radius = [r * 1.1 for r in ring_radius]
        canvas_size = int(canvas_size * 1.1)
        center_x = center_y = canvas_size // 2

        max_ring_radius = canvas_size // 2
        if ring_radius[-1] > max_ring_radius:
            ring_radius = [r * (max_ring_radius / ring_radius[-1]) for r in ring_radius]
    
    log_debug("Maximum adjustment attempts reached. Using the last adjusted sizes.")
    return placed_entries, medium_font, small_font, ring_radius, center_x, center_y, canvas_size

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

def initial_placement(entries, quadrants, ring_radius, center_x, center_y, font):
    """Place nodes initially based on their quadrants and rings."""
    placed_entries = []
    for entry in entries:
        try:
            quadrant_index = next((i for i, q in enumerate(quadrants) if q['id'] == entry['quadrant']), None)
            if quadrant_index is None:
                raise ValueError(f"Quadrant {entry['quadrant']} not found for entry {entry['title']}")
            
            product_name = entry["title"]
            ring_name = entry['timeline'][0]['ring']
            ring_index = next((i for i, r in enumerate(ring_radius) if r['id'] == ring_name), None)
            if ring_index is None:
                raise ValueError(f"Ring {ring_name} not found for entry {product_name}")

            angle_start = quadrant_index * quadrant_angle_step
            angle_end = angle_start + quadrant_angle_step
            angle = random.uniform(angle_start, angle_end)

            if ring_name == "adopt":
                radius = random.uniform(0, ring_radius[0] - 5)
            else:
                radius = random.uniform(ring_radius[ring_index - 1], ring_radius[ring_index] - 5) if ring_index > 0 else random.uniform(0, ring_radius[ring_index] - 5)

            x = center_x + radius * cos(radians(angle))
            y = center_y + radius * sin(radians(angle))
            text_width, text_height = calculate_text_size(entry, font)
            placed_entries.append([x, y, text_width, text_height, quadrant_index, ring_index, entry])
            log_debug(f"Placed {product_name} at x={x}, y={y}, quadrant_index={quadrant_index}, ring_index={ring_index}")
        except ValueError as e:
            log_debug(f"Error in initial placement: {e}")
    
    return placed_entries

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
                    distance = sqrt(dx * dx + dy * dy) + 0.1
                    min_distance = (wi + wj) / 2 + (hi + hj) / 2
                    if distance < min_distance:
                        repulsion = REPULSION_CONSTANT / (distance * distance)
                        fx += repulsion * (dx / distance)
                        fy += repulsion * (dy / distance)

            original_x, original_y = initial_placement_position(entry_i, quadrants, rings, center_x, center_y, ring_radius)
            dx = original_x - xi
            dy = original_y - yi
            distance = sqrt(dx * dx + dy * dy)
            attraction = ATTRACTION

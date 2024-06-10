import json
import math
import os
import requests
import textwrap
import random
from math import cos, sin, radians
from PIL import Image, ImageDraw, ImageFont # Function to download the font if it doesn't exist

def download_font(url, font_path):
    if not os.path.exists(font_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(font_path, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception(f"Failed to download font from {url} (status code: {response.status_code})")

CANVAS_SIZE=1800
placed_entries=[]
# Download the font if necessary
font_url = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf" #needs updating
font_path = "fonts/Roboto-Regular.ttf"
download_font(font_url, font_path)

# Load the font with error handling
try:
    large_font = ImageFont.truetype(font_path, 32)
    font = ImageFont.truetype(font_path, 18)
    small_font = ImageFont.truetype(font_path, 12)
except IOError:
    print("Error loading font. Using default font.")
    font = ImageFont.load_default(28)
    large_font = ImageFont.load_default(12)
    small_font = ImageFont.load_default(8)

# Load json data
with open('product-definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('radar-categories.json', 'r') as f:
    category_titles = json.load(f)

with open('tr_product-radarstatus.json', 'r') as f:
    classifications = json.load(f)

# Define quadrants based on category titles, this is a bit all the wrong way around
# TODO: This should all be taken by tr_product-classifications.json but I need to refactor it
quadrants = [
    { "index": 0, "id": "data_ml", "quadrant_name": "Data Platform" },
    { "index": 1, "id": "storage", "quadrant_name": "Storage and Databases" },
    { "index": 2, "id": "compute", "quadrant_name": "Compute and Web Platform" },
    { "index": 3, "id": "build_ci", "quadrant_name": "DevOps" },
    { "index": 4, "id": "observability", "quadrant_name": "Observability" }
]

# Define rings to appear on the radar for "status" of the tech
rings = [
    { "index": 0, "id": "adopt", "name": "Adopt", "color": "#93c47d" },
    { "index": 1, "id": "evaluation", "name": "Assess", "color": "#fbdb84" },
    { "index": 2, "id": "hold", "name": "Hold", "color": "#efafa9" },
    { "index": 3, "id": "retire", "name": "Retire", "color": "#a32d01" }
]

# Map categories to slices of the circular tech radar
category_to_quadrant = {
    "Data Platform": 0,
    "Storage and Databases": 1,
    "Compute and Web Platform": 2,
    "DevOps": 3,
    "Observability": 4
}

# Map products to rings based on classifications json file
product_to_ring = {}
for id, products in classifications.items():
     for product in products:
         product_to_ring[product] = id
         print(product,id)

# Transform entries
entries = []
for product_key, product in product_definitions.items():
    quadrant_id = category_to_quadrant.get(product.get('category'))
    keywords = product.get('keywords', []).join(' ')
    ring = product_to_ring.get(product_key)
    entry = {
        "id": product_key,
        "title": product['name'],
        "description": product.get('description', ''),
        "url": product.get('url', ''),
        "file_path": product.get('file_path', ''),
        "quadrant_id": quadrant_id,
        "quadrand_name": product.get('category'),
        "keywords": keywords,
        "ring": ring,
        "image_url": product.get('image_url', '')
    }
    print (entry)
    entries.append(entry)

# Construct the final data model
tech_radar = {
    "title": "Cloud Tech Radar",
    "quadrants": quadrants,
    "rings": rings,
    "entries": entries
}

# Function to resize and add images
def add_images(entry, draw,image, x, y):
    try:
        local_img_path = f'{entry.get("file_path")}'
        
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

        opacity_level = 0 #doesn't seem to work
        img = Image.open(local_img_path).convert("RGBA")
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        new_height = 38  #vary based on the content in your tech radar..
        new_width = int(new_height * img_ratio)
        img2 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        img_x = x - new_width // 2
        img_y = y - new_height // 2
        image.paste(img2, (int(img_x), int(img_y)))
        placed_entries.append((img_x,img_y))
        return int(img_x), int(img_y), new_width, new_height
    except FileNotFoundError:
        print(f"Image file for {entry['id']} not found.")
    except IOError:
        print(f"Error opening image for {entry['id']}.")
    except Exception as e:
        print(f"Error adding image for {entry['id']}: {e}")
    return None, None, None, None

# Draw the tech radar
def draw_tech_radar(tech_radar):
    width, height = CANVAS_SIZE, CANVAS_SIZE# Set canvas size
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    random.seed(200) 
    center_x, center_y =((width // 2), (height // 2))
    ring_radius = [360, 475, 595, 680]

    quadrant_angle_step = 360 / len(tech_radar['quadrants'])
    
    # Draw quadrants and their titles
    for i, quadrant in enumerate(tech_radar.items()):
        angle = i *  quadrant_angle_step
        name = quadrants.get('quadrant_name')
        x = center_x + ring_radius[-1] * cos(radians(angle + quadrant_angle_step / 2))
        y = center_y + ring_radius[-1] * sin(radians(angle + quadrant_angle_step / 2)) 
        draw.text((x, y), quadrant.quadrand_name, font=large_font, fill="black", anchor="mm")
        placed_entries.append((x,y))

    # Draw rings and their titles
    for ring in tech_radar['rings']:
        radius = ring_radius[tech_radar['rings'].index(ring)]
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=ring['color'], width=3)
        draw.text((center_x + radius, center_y), ring['name'], font=font, fill="black", anchor="mm")
        placed_entries.append((center_x + radius, center_y))
        placed_entries.append((center_x + radius-10, center_y))

    # Calculate the number of products in each quadrant at each ring level
    # Calculate the number of products in each quadrant at each ring level
    quadrant_ring_counts = {q['id']: {i: 0 for i in range(len(ring_radius))} for q in quadrants}

    for entry in tech_radar['entries']:
        quadrant_id = entry['quadrant_id']
        ring_index = rings.index(next(r for r in rings if r['id'] == entry['ring']))
        if quadrant_id in quadrant_ring_counts:
            quadrant_ring_counts[quadrant_id][ring_index] += 1

    print(quadrant_ring_counts)

    # Place each product with evenly spaced angles
    #for quadrant_index, quadrant in enumerate(quadrants):
    for ring_index, radius in enumerate(ring_radius):
        products_in_quadrant_ring = [
            entry for entry in tech_radar 
            if entry['quadrant_id'] == quadrant['id'] and entry['ring_index'] == ring_index
        ]
        
        if not products_in_quadrant_ring:
            continue
        
        # Use the already calculated quadrant_angle_step
        angle_offset = quadrant_angle_step / len(products_in_quadrant_ring)
        
        for i, entry in enumerate(products_in_quadrant_ring):
            angle = quadrant_index * quadrant_angle_step + (i * angle_offset)
            text_x = center_x + radius * math.cos(math.radians(angle))
            text_y = center_y + radius * math.sin(math.radians(angle))
            
            # Place image and text
            img_x, img_y, img_w, img_h = add_images(entry, draw, img, text_x, text_y)
            if img_x is not None:
                placed_entries.append((text_x, text_y))
                draw.text((img_x + img_w / 2 + 5 , img_y - img_h / 2 + 5), entry['name'], font=font, fill="black", anchor="mm")
                draw.text((img_x - img_w / 2 - 12, img_y + img_h / 2 + 12), f"{textwrap.fill(entry['description'], 24)}", font=small_font, fill="black")
                placed_entries.append((img_x + img_w / 2 + 5, img_y - img_h / 2 + 5))
                placed_entries.append((img_x - img_w / 2 - 12 , img_y + img_h / 2 + 12))

    img.save('output/tech_radar.png')
    print("Tech Radar image saved to tech_radar.png")


draw_tech_radar(tech_radar)


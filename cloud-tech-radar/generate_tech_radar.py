import json
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

placed_entries=[]
# Download the font if necessary
font_url = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
font_path = "Roboto-Regular.ttf"
download_font(font_url, font_path)

# Load the font with error handling
try:
    large_font = ImageFont.truetype(font_path, 42)
    font = ImageFont.truetype(font_path, 24)
    small_font = ImageFont.truetype(font_path, 14)
except IOError:
    print("Error loading font. Using default font.")
    font = ImageFont.load_default(20)
    large_font = ImageFont.load_default(44)
    small_font = ImageFont.load_default(14)

# Load data
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('tech_radar_product_categories.json', 'r') as f:
    category_titles = json.load(f)

with open('tech_radar_classifications.json', 'r') as f:
    classifications = json.load(f)

# Define quadrants based on category titles
quadrants = [
    { "id": "data_ml", "name": "Data Platform" },
    { "id": "storage", "name": "Storage and Databases" },
    { "id": "compute", "name": "Compute and Web Platform" },
    { "id": "build_ci", "name": "DevOps" },
    { "id": "observability", "name": "Observability" }
]

# Define rings
rings = [
    { "id": "adopt", "name": "Adopt", "color": "#93c47d" },
    { "id": "evaluation", "name": "Assess", "color": "#fbdb84" },
    { "id": "hold", "name": "Hold", "color": "#efafa9" },
    { "id": "retire", "name": "Retire", "color": "#a32d01" }
]

# Map categories to quadrants
category_to_quadrant = {
    "Data Platform": "data_ml",
    "Storage and Databases": "storage",
    "Compute and Web Platform": "compute",
    "DevOps": "build_ci",
    "Observability": "observability"
}

# Map products to rings based on classifications
product_to_ring = {}
for classification, products in classifications.items():
    for product in products:
         product_to_ring[product] = classification
         print (product, classification)

# Function to clean the text
def clean_text(text):
    return text#.replace('(', '').replace(')', '').strip()

# Transform entries
entries = []
for product_key, product in product_definitions.items():
    quadrant = category_to_quadrant.get(product.get('category'))
    keywords = product.get('keywords', []).join(' ')
    entry = {
        "id": product_key,
        "title": product['name'],
        "description": product.get('description', ''),
        "url": product.get('url', ''),
        "file_path": product.get('file_path', ''),
        "quadrant": quadrant,
        "keywords": keywords,
        "image_url": product.get('image_url', '')
    }
    entries.append(entry)

# Construct the final data model
tech_radar = {
    "title": "RG Cloud Tech Radar",
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

        opacity_level = 70
        img = Image.open(local_img_path).convert("RGBA")
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        new_height = 90
        new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        img_x = x - new_width // 2
        img_y = y - new_height // 2
        image.paste(img, (int(img_x), int(img_y)))
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
    width, height = 2400, 2200# Set canvas size
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    random.seed(10000) 
    center_x, center_y = ((width // 2), (height // 2))
    ring_radius = [460, 670, 820, 1000 ]

    quadrant_angle_step = 360 / len(tech_radar['quadrants'])
    
    # Draw quadrants and their titles
    for i, quadrant in enumerate(tech_radar['quadrants']):
        angle = i * quadrant_angle_step
        x = center_x + ring_radius[-1] * cos(radians(angle + quadrant_angle_step / 2))
        y = center_y + ring_radius[-1] * sin(radians(angle + quadrant_angle_step / 2)) 
        draw.text((x, y), quadrant['name'], font=large_font, fill="black", anchor="mm")
        placed_entries.append((x,y))
        placed_entries.append((x-30,y-5))
        placed_entries.append((x+30,y+5))

    # Draw rings and their titles
    for ring in tech_radar['rings']:
        radius = ring_radius[tech_radar['rings'].index(ring)]
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline=ring['color'], width=4)
        draw.text((center_x + radius, center_y), ring['name'], font=font, fill="black", anchor="mm")
        placed_entries.append((center_x + radius, center_y))
        placed_entries.append((center_x + radius-10, center_y))
        placed_entries.append((center_x + radius+10, center_y))

    random.seed(42)
    for entry in tech_radar['entries']:
        quadrant_index = next(i for i, q in enumerate(tech_radar['quadrants']) if q['id'] == entry['quadrant'])
        product_name = entry["title"]
        ring_name = product_to_ring[product_name]  # Default to 'hold' if not found
        if ring_name is None:
            ring_name = 'hold'
        ring_index = next(i for i, r in enumerate(tech_radar['rings']) if r['id'] == ring_name)
    
        
        angle_start = quadrant_index * quadrant_angle_step
        angle_end = angle_start + quadrant_angle_step
        angle = (angle_start + angle_end) / 2  # Center angle of the quadrant section
        random_factor = random.randint(-110,110)/100 * angle 
        radius = ring_radius[ring_index] - 20
        print (random_factor)
        angle = (angle_start+angle_end)/2 + random_factor
        x = center_x + radius * cos(radians(angle))
        y = center_y + radius * sin(radians(angle))
        print (x,y)
        i=0       
        totalanglechange=0
        maxanglechange=quadrant_angle_step/2+20 #since we're at the radius
        collision = any(abs(px - x) < 110 and abs(py - y) < 110 for px, py in placed_entries)
        while collision:
            i+=1
            print (x,y)
            angle = random.randint(-20,20)
            if abs(angle+totalanglechange) > maxanglechange:
                angle-=maxanglechange
                totalanglechange=angle
            else:
                totalanglechange+=angle
            x += cos(radians(angle)) 
            y += sin(radians(angle)) 
            print (x,y)
            collision = any(abs(px - x) < (110) and abs(py - y) < (110) for px, py in placed_entries)
        
        img_x, img_y, img_w,img_h = add_images(entry, draw, img, x, y)
        if img_x is not None:
             placed_entries.append((img_x,img_y))
             placed_entries.append((img_x-img_w/2, img_y-img_y/2))
             placed_entries.append((img_x+img_w/2, img_y-img_y/2))
             placed_entries.append((img_x-img_w/2, img_y+img_y/2))
             placed_entries.append((img_x+img_w/2, img_y+img_y/2))
             draw.text((img_x-img_w/2+1, img_y - img_h -10), entry['title'], font=font, fill="black", anchor="mm")
#             draw.text((img_x-img_w/2+1, img_y + img_h + 2), f"{entry['keywords']}", font=small_font, fill="black")
             placed_entries.append((img_x+img_w/2+1, img_y + img_h + 10))
             draw.text((img_x-img_w/2-5, img_y - img_h + 3), f"{textwrap.fill(entry['description'],45)}", font=small_font, fill="black")
             placed_entries.append((img_x-img_w/2+1, img_y - img_h +3))

    img.save('tech_radar.png')
    print("Tech Radar image saved to tech_radar.png")

draw_tech_radar(tech_radar)


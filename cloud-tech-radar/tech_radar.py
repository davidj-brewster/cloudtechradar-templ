import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# Load product definitions and tech radar classifications from JSON files
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('tech_radar_classifications.json', 'r') as f:
    tech_radar_classifications = json.load(f)

# Define the categories and colors
categories = {
    "Data/ML": "#E8F5E9",
    "Storage": "#FFF3E0",
    "Compute/GKE": "#E3F2FD",
    "Build Products": "#F3E5F5"
}

# Define image size and create a new image with white background
image_width = 1500
image_height = 2000
background_color = "#FFFFFF"
img = Image.new('RGB', (image_width, image_height), background_color)
draw = ImageDraw.Draw(img)

# Define fonts
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust the path if needed
font_title = ImageFont.truetype(font_path, 24)
font_category = ImageFont.truetype(font_path, 20)
font_product = ImageFont.truetype(font_path, 16)
font_use_case = ImageFont.truetype(font_path, 12)

# Set starting positions
x_offset = 50
y_offset = 50

# Draw categories and products
for category, color in categories.items():
    # Draw category heading
    draw.rectangle([(x_offset - 10, y_offset - 10), (image_width - x_offset, y_offset + 40)], fill=color)
    draw.text((x_offset, y_offset), category, font=font_category, fill="black")
    y_offset += 50

    # Draw products under the category
    for product in tech_radar_classifications.get(category, []):
        details = product_definitions[product]
        # Download and resize the image
        response = requests.get(details["image_url"])
        img_product = Image.open(BytesIO(response.content))
        img_product.thumbnail((50, 50), Image.ANTIALIAS)

        # Draw the product image
        img.paste(img_product, (x_offset, y_offset))

        # Draw the product name and URL
        draw.text((x_offset + 60, y_offset), details["name"], font=font_product, fill="black")
        draw.text((x_offset + 60, y_offset + 20), details["url"], font=font_use_case, fill="blue")

        # Draw example use cases
        draw.text((x_offset + 60, y_offset + 40), ", ".join(details["example_use_cases"]), font=font_use_case, fill="gray")

        y_offset += 80

# Save the final image
img.save('tech_radar_updated.png')


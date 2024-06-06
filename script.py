import os

# Define the file content
readme_content = """
# Cloud Tech Radar

This project generates a graphical representation of a cloud tech radar, categorizing various cloud technologies into "adopt," "evaluation," "hold," and "retire" categories. The script uses Python to fetch product images, resize them, and create a tech radar image.

## Features

- Fetches and resizes product images
- Categorizes products into four categories: adopt, evaluation, hold, retire
- Generates a tech radar image
- Configurable through JSON files for easy updates

## Prerequisites

- Python 3.x
- Python libraries: `requests`, `PIL`, `matplotlib`

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/cloud-tech-radar.git
    cd cloud-tech-radar
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\\Scripts\\activate`
    ```

3. **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure the products and classifications:**
    - Edit `product_definitions.json` to define the products with their names, URLs, and image URLs.
    - Edit `tech_radar_classifications.json` to classify the products into the desired categories.

2. **Run the script:**
    ```bash
    python tech_radar.py
    ```

3. **View the generated tech radar image:**
    - The image will be saved as `tech_radar.png` in the current directory.

## JSON Files

### `product_definitions.json`

This file contains the definitions of all products used in the tech radar. Each product has a name, URL, and image URL. Example:

{
    "BigQuery": {
        "name": "BigQuery",
        "url": "https://cloud.google.com/bigquery",
        "image_url": "https://cloud.google.com/images/products/logos/svg/bigquery.svg"
    },
    "Firestore": {
        "name": "Firestore",
        "url": "https://cloud.google.com/firestore",
        "image_url": "https://cloud.google.com/images/products/logos/svg/firestore.svg"
    }
}

### `tech_radar_classifications.json`

This file classifies the products into categories: adopt, evaluation, hold, and retire. Example:

{
    "adopt": [
        "BigQuery"
    ],
    "hold": [
        "Firestore"
    ],
    "evaluation": [],
    "retire": []
}

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or issues, please open an issue in this repository or contact the maintainer.
"""

requirements_content = """
requests
Pillow
matplotlib
"""

tech_radar_py_content = """
import json
import logging
import requests
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
IMAGE_SIZE = (50, 50)
RADAR_SIZE = (1000, 1000)
FONT_SIZE = 12

def fetch_and_resize_image(image_url):
    \"\"\"Fetches an image from the URL and resizes it.\"\"\"
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        image = image.resize(IMAGE_SIZE)
        return image
    except requests.RequestException as e:
        logging.error(f"Error fetching image from {image_url}: {e}")
        return None

def create_radar_chart(products, classifications):
    \"\"\"Creates a radar chart image with the given products and classifications.\"\"\"
    radar_image = Image.new('RGB', RADAR_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(radar_image)
    font = ImageFont.load_default()

    # Define positions for categories
    category_positions = {
        'adopt': (200, 200),
        'evaluation': (600, 200),
        'hold': (200, 600),
        'retire': (600, 600)
    }

    for category, items in classifications.items():
        logging.info(f"Processing category: {category}")
        x, y = category_positions[category]

        for i, product_key in enumerate(items):
            product = products.get(product_key, None)
            if not product:
                logging.warning(f"Product {product_key} not found in product definitions")
                continue
            
            logging.info(f"Processing product: {product['name']}")

            # Fetch and resize the image
            image = fetch_and_resize_image(product['image_url'])
            if image:
                radar_image.paste(image, (x, y + i * (IMAGE_SIZE[1] + 10)))

            # Draw the product name and URL
            text_position = (x + IMAGE_SIZE[0] + 10, y + i * (IMAGE_SIZE[1] + 10))
            draw.text(text_position, product['name'], fill=(0, 0, 0), font=font)
            draw.text((text_position[0], text_position[1] + 15), product['url'], fill=(0, 0, 0), font=font)

    return radar_image

def save_radar_image(image, filepath='tech_radar.png'):
    \"\"\"Saves the radar image to a file.\"\"\"
    try:
        image.save(filepath)
        logging.info(f"Tech radar image saved to {filepath}")
    except Exception as e:
        logging.error(f"Error saving image: {e}")

def main():
    # Load product definitions and classifications
    with open('product_definitions.json') as f:
        products = json.load(f)
    
    with open('tech_radar_classifications.json') as f:
        classifications = json.load(f)
    
    # Create radar chart
    radar_image = create_radar_chart(products, classifications)
    
    # Save radar image
    save_radar_image(radar_image)

# Main script execution
if __name__ == "__main__":
    main()
"""

product_definitions_json_content = """
{
    "BigQuery": {
        "name": "BigQuery",
        "url": "https://cloud.google.com/bigquery",
        "image_url": "https://cloud.google.com/images/products/logos/svg/bigquery.svg"
    },
    "Firestore": {
        "name": "Firestore",
        "url": "https://cloud.google.com/firestore",
        "image_url": "https://cloud.google.com/images/products/logos/svg/firestore.svg"
    }
}
"""

tech_radar_classifications_json_content = """
{
    "adopt": [
        "BigQuery"
    ],
    "hold": [
        "Firestore"
    ],
    "evaluation": [],
    "retire": []
}
"""

# Create the directory for the files
os.makedirs('cloud-tech-radar', exist_ok=True)

# Write the files
with open('cloud-tech-radar/README.md', 'w') as readme_file:
    readme_file.write(readme_content)

with open('cloud-tech-radar/requirements.txt', 'w') as requirements_file:
    requirements_file.write(requirements_content)

with open('cloud-tech-radar/tech_radar.py', 'w') as tech_radar_py_file:
    tech_radar_py_file.write(tech_radar_py_content)

with open('cloud-tech-radar/product_definitions.json', 'w') as product_definitions_file:
    product_definitions_file.write(product_definitions_json_content)

with open('cloud-tech-radar/tech_radar_classifications.json', 'w') as tech_radar_classifications_file:
    tech_radar_classifications_file.write(tech_radar_classifications_json_content)

# Display the content of each file
with open('cloud-tech-radar/README.md', 'r') as file:
    print("README.md:")
    print(file.read())

with open('cloud-tech-radar/requirements.txt', 'r') as file:
    print("\nrequirements.txt:")
    print(file.read())

with open('cloud-tech-radar/tech_radar.py', 'r') as file:
    print("\ntech_radar.py:")
    print(file.read())

with open('cloud-tech-radar/product_definitions.json', 'r') as file:
    print("\nproduct_definitions.json:")
    print(file.read())

with open('cloud-tech-radar/tech_radar_classifications.json', 'r') as file:
    print("\ntech_radar_classifications.json:")
    print(file.read())


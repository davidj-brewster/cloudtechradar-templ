
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
- Font file Roboto-Regular.ttf


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/rg-dbrewste/cloud-tech-radar.git
    cd cloud-tech-radar
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure the products and classifications:**
    - Edit `product_definitions.json` to define the products with their names, URLs. You don't need to search for the image URLs but can instead use the `update_images.py` script which will search for images for the products in your configuration and download some images to product_images subdirectory.
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

This file classifies the products into categories: adopt, evaluation, hold, and retire. 
Example:

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

### `tech_radar_classifications.json`

This file classifies the products into categories: adopt, evaluation, hold, and retire. 
Example:

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


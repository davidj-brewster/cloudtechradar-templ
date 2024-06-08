
# Cloud Tech Radar

This project generates a graphical representation of a cloud tech radar, categorizing various cloud technologies into "adopt," "evaluation," "hold," and "retire" categories. The script uses Python to fetch product images, resize them, and create a tech radar image.

## Features

- Fetches and resizes product images
- Categorizes products into four categories: adopt, evaluation, hold, retire
- Generates a tech radar image
- Configurable through JSON files for easy updates
- This data structure can be translated through the included tooling to Backstage-compatible YAML format, to a Mermaid diagram or directly through the tooling to a reasonable looking PNG image directly through the Python process.
- Future plans are to allow splices of the tech radar (e.g., based on Component metadata) to be visualised separately to help create documentation relevant to a specific team or function

## Prerequisites

- Python 3.x
- Python virtualenv, package requirements are listed in requirements.txt
- Font file Roboto-Regular.ttf (or  a replacement of your choosing)


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

1. **Configure the categories, products and classifications:**
    - Create or edit `tech_radar_product_categories.json` - each category will get a "vertical" slice of the tech radar pie chart, so avoid having too many as it can result in needing to make the diagrams massive or lots of components cramming together. I think more than 5 or 6 would not render that well. Product categories can be whatever you make them. Business-area focussed, highly specific technically, or diffentiating software vs infastructure stacks. 
    - Create or edit `product_definitions.json` which defines the products with their names, URLs. You don't need to search for the product icon image URLs - there is a helper script which will take the name, description and example use-cases from the file, then search and download the (hopefully) most relevant product images to product_images subdirectory (of course, double check the output on common terms like "cloud storage", though).
    - Create or edit `tech_radar_classifications.json` to classify the products into your desired categories in terms of their product lifecycle. 


2. **Run the script:**
    ```bash
    python3 generate_tech_radar.py
    ```

3. **View the generated tech radar image:**
    - The image will be saved as `tech_radar.png` in the ./output directory.

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


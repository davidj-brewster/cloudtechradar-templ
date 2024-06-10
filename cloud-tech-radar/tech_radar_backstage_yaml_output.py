import json

# Load data
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('product_categories.json', 'r') as f:
    category_titles = json.load(f)

with open('radar_classifications.json', 'r') as f:
    classifications = json.load(f)

# TODO: this data is already in radar_classifications.json...
# Define quadrants based on category titles
quadrants = [
    { "id": "data_ml", "name": "Big Data" },
    { "id": "storage", "name": "Storage and Databases" },
    { "id": "compute", "name": "Compute and Web Platform" },
    { "id": "build_ci", "name": "DevOps" },
    { "id": "observability", "name": "Observability" }
]

# TODO: This can be dynamic based on what an organisation wants to 
# Define rings
rings = [
    { "id": "adopt", "name": "Adopt", "color": "#93c47d" },
    { "id": "trial", "name": "Trial", "color": "#93d2c2" },
    { "id": "assess", "name": "Assess", "color": "#fbdb84" },
    { "id": "hold", "name": "Hold", "color": "#efafa9" }
]

# Map categories to quadrants
# AGAIN, this is just lazy me .. will be fixed 
category_to_quadrant = {
    "Big Data": "data_ml",
    "Storage and Databases": "storage",
    "Compute and Web Platform": "compute",
    "DevOps": "build_ci",
    "Observability": "observability",
}

# Transform entries
entries = []
for product_key, product in product_definitions.items():
    quadrant = category_to_quadrant.get(product['category'])
    ring = classifications.get(product_key, {}).get('ring', 'hold')  # Default to 'hold' if not specified
    entry = {
        "id": product_key,
        "title": product['name'],
        "description": product.get('description', ''),
        "key": product_key,
        "url": product.get('url', ''),
        "quadrant": quadrant,
        "timeline": [
            { "ring": ring, "date": "2023-06-07" }  # Example date
        ]
    }
    entries.append(entry)

# Construct the final data model
tech_radar = {
    "title": "Tech Radar",
    "quadrants": quadrants,
    "rings": rings,
    "entries": entries
}

# Save the output to a file
output_path = 'output/tech_radar_backstage_cloud.json'
with open(output_path, 'w') as f:
    json.dump(tech_radar, f, indent=4)

print(f"Backstage Tech Radar JSON saved to {output_path}")



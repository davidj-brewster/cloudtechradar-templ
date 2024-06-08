import json

# Load product definitions and tech radar categories from JSON files
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('tech_radar_product_categories.json', 'r') as f:
    category_titles = json.load(f)

# Create the mermaidJS output for a mind map
mermaid_output = """
mindmap
root((Tech Radar))
"""

# Function to clean the product names and keywords
def clean_text(text):
    return text.replace('(', '').replace(')', '')

# Add products under each category
for category, title in category_titles.items():
    print(f"Processing category: {category} -> {title}")
    mermaid_output += f"  {title}\n"
    for product_key, product in product_definitions.items():
        if product.get('category') == category:
            # Clean the product name and keywords
            product_name = clean_text(product['name'])
            keywords = clean_text(product['keywords'])
            product_info = f"    {product_name}: {keywords}\n"
            mermaid_output += product_info
            print(f"  Added product: {product_key}")

# Save the mermaidJS output to a file
# use either github or mermaid's own viewer to preview what it looks like
output_path = 'output/tech_radar.mmd'
with open(output_path, 'w') as f:
    f.write(mermaid_output)


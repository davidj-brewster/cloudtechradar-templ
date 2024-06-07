import json

# Load product definitions and tech radar categories from JSON files
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('tech_radar_product_categories.json', 'r') as f:
    category_titles = json.load(f)

# Create the mermaidJS output
mermaid_output = """
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fff', 'edgeLabelBackground':'#fff', 'tertiaryColor': '#fff'}}}%%
graph TD
"""

# Add products under each category
for category, title in category_titles.items():
    print(f"Processing category: {category} -> {title}")
    mermaid_output += f"\n    subgraph \"{title}\"\n        direction TB\n"
    for product_key, product in product_definitions.items():
        if product.get('category') == category:
            use_cases = ", ".join(product["example_use_cases"])
            # Unique identifier for each node
            node_id = product_key.replace(" ", "_").replace("/", "_").replace("&", "and")
            product_info = f"{node_id}[\"{product['name']}\\nURL: {product['url']}\\nDescription: {product['description']}\\nUse Cases: {use_cases}\"]"
            mermaid_output += f"        {product_info}\n"
            print(f"  Added product: {product_key}")
    mermaid_output += "    end\n"

# Save the mermaidJS output to a file
output_path = 'tech_radar.mmd'
with open(output_path, 'w') as f:
    f.write(mermaid_output)

print(f"Mermaid.js output saved to {output_path}")


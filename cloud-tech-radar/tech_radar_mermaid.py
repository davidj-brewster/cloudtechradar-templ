import json

# Load product definitions and tech radar classifications from JSON files
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

with open('tech_radar_classifications.json', 'r') as f:
    tech_radar_classifications = json.load(f)

# Define the categories
categories = ["Data/ML", "Storage", "Compute/GKE", "Build Products"]

# Create the mermaidJS output
mermaid_output = """
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fff', 'edgeLabelBackground':'#fff', 'tertiaryColor': '#fff'}}}%%
graph TB
    classDef category fill:#f9f,stroke:#333,stroke-width:2px;
"""

# Add products under each category
for category in categories:
    mermaid_output += f"\n    subgraph {category}\n        direction TB\n"
    for product in tech_radar_classifications.get(category, []):
        details = product_definitions[product]
        use_cases = ", ".join(details["example_use_cases"])
        product_info = f"{product}['{details['name']}\\nURL: {details['url']}\\nUse Cases: {use_cases}']"
        mermaid_output += f"        {product_info}\n"
    mermaid_output += "    end\n"

# Save the mermaidJS output to a file
output_path = 'tech_radar.mmd'
with open(output_path, 'w') as f:
    f.write(mermaid_output)

print(f"Mermaid.js output saved to {output_path}")


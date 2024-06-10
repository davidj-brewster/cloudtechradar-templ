import json
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os
from bs4 import BeautifulSoup
import re
import shutil

# Load the existing product_definitions.json
with open('product_definitions.json', 'r') as f:
    product_definitions = json.load(f)

# Backup the original product_definitions.json
shutil.copy('product_definitions.json', 'product_definitions_backup.json')

# Function to validate and download image
def validate_and_download_image(product, url, version=0):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img_format = img.format.lower()
        img_path = os.path.join("product_images", f"{product}_{version}.{img_format}")
        img.save(img_path)
        width, height = img.size
        if width < 80 or height < 80: 
          return False, None, None
        return True, img_path, url
    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Error fetching image from {url}: {e}")
        return False, None, None

# Function to search for alternative image URLs
def search_alternative_image_url(product):
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={product.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all("img", {"src": re.compile("http*")})
        for img_tag in img_tags:
            img_url = img_tag['src']
            success, img_path, final_url = validate_and_download_image(product, img_url)
            if success:
                return img_url
        return None
    except Exception as e:
        print(f"Error searching for alternative image URL for {product}: {e}")
        return None

# Directory to save images
os.makedirs("product_images", exist_ok=True)

# Validate and update URLs in product_definitions.json
updated_products = []
for product, details in product_definitions.items():
    url = details["image_url"]
    i=0
    j=0
    while True:
        success, image_path, final_url = validate_and_download_image(product, url)
        if success:
            if i==0:
              product_definitions[product]["image_url"] = final_url
              product_definitions[product]["file_path"] = image_path
              updated_products.append(product)
              print(f"Downloaded image for {product}: {final_url}")
              i+=1
              alternative_url = search_alternative_image_url(product)
              validate_and_download_image(product, alternative_url,1)
              alternative_url = search_alternative_image_url(product)
              validate_and_download_image(product, alternative_url,2)
              break
        else:
            print(f"Searching for alternative URL for {product}...")
            alternative_url = search_alternative_image_url(product)
            if alternative_url:
                url = alternative_url
            else:
                j+=1
                if j==2:
                  print(f"Could not find a valid URL for {product}")
                  break

# Save the updated product_definitions.json
with open('product_definitions.json', 'w') as f:
    json.dump(product_definitions, f, indent=4)

# Display the updated products
print("Updated products:")
for product in updated_products:
    print(f"{product}")


import pandas as pd
from bs4 import BeautifulSoup
import requests

# List to store individual product attributes
products = []

for n in range(1, 3):  # Loop through pages
    url = "https://charcoal.com.pk/collections/jacket?page=" + str(n)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    box = soup.find("product-list", class_ = "product-list")

    print(f"Scraping URL: {url}")
   
    if not box:
        print(f"No products found on page {n}")
        continue

    # Extract all product containers from the page
    product_containers = box.find_all("product-card", class_="product-card")  # Replace "p-item" with the class that wraps each product if needed

    # print(f"product_containers: {product_containers}")
    print("\n")
    print("\n")
    print("\n")
    print("\n")

    for product in product_containers:
        # Initialize a dictionary for each product
        product_data = {
            "name": None,
            "actual price": None,
            "current price": None,
            "post link": None,
        }

        # Extract name
        name_tag = product.find("span", class_="product-card__title").find("a")
        if name_tag:
            product_data["name"] = name_tag.text.strip()
            print(product_data["name"])


        # Extract actual price
        actual_price_tag = product.find("compare-at-price", class_="text-subdued")
        if actual_price_tag:
            full_text = actual_price_tag.text.strip()
            product_data["actual price"] = full_text.replace("Regular price", "").strip()
            print(product_data["actual price"])


        # Extract current price
        current_price_tag = product.find("sale-price", class_="text-subdued")
        if current_price_tag:
            full_text = current_price_tag.text.strip()
            product_data["current price"] = full_text.replace("Sale price", "").strip()
            print(product_data["current price"])

        # Find the <a> tag
        product_tag = product.find("a", class_="bold")
        if product_tag:
            # Extract the href attribute
            product_data["post link"] = "https://charcoal.com.pk"+product_tag.get("href")
            print("post link:", product_data["post link"])

        # Add the product data to the list
        products.append(product_data)

    print(f"Scraped {len(product_containers)} products from page {n}")
    print("\n")

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(products)

# Display the DataFrame
print(df)

# Optionally save to a CSV
df.to_csv("ecommerce_products.csv", index=False)

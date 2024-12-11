import pandas as pd
from bs4 import BeautifulSoup
import requests

# List to store individual product attributes
products = []

for n in range(2, 20):  # Loop through pages
    url = "https://priceoye.pk/bluetooth-speakers?page=" + str(n)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    box = soup.find("div", class_="filter-blist-sec")

    print(f"Scraping URL: {url}")

    if not box:
        print(f"No products found on page {n}")
        continue

    # Extract all product containers from the page
    product_containers = box.find_all("div", class_="productBox b-productBox")  # Replace "p-item" with the class that wraps each product if needed

    for product in product_containers:
        # Initialize a dictionary for each product
        product_data = {
            "name": None,
            "actual price": None,
            "current price": None,
            "rating": None,
            "reviews": None,
        }

        # Extract name
        name_tag = product.find("div", class_="p-title bold h5")
        if name_tag:
            product_data["name"] = name_tag.text.strip()

        # Extract actual price
        actual_price_tag = product.find("div", class_="price-diff-retail")
        if actual_price_tag:
            product_data["actual price"] = actual_price_tag.text.strip()

        # Extract current price
        current_price_tag = product.find("div", class_="price-box p1")
        if current_price_tag:
            product_data["current price"] = current_price_tag.text.strip()

        # Extract rating
        rating_tag = product.find("span", class_="h6 bold")
        if rating_tag:
            product_data["rating"] = rating_tag.text.strip()

        # Extract reviews
        reviews_tag = product.find("span", class_="rating-h7 bold")
        if reviews_tag:
            product_data["reviews"] = reviews_tag.text.strip()

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

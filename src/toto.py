import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# product_page_url
product_page_url = url

# title
title = soup.find("div", class_="product_main").h1.text.strip()

# table des informations
table = soup.find("table", class_="table table-striped")
rows = table.find_all("tr")
data = {row.th.text.strip(): row.td.text.strip() for row in rows}

# universal_product_code (upc)
upc = data.get("UPC")

# price_including_tax
price_including_tax = data.get("Price (incl. tax)")

# price_excluding_tax
price_excluding_tax = data.get("Price (excl. tax)")

# number_available
availability_text = data.get("Availability", "")
number_available = int(''.join(filter(str.isdigit, availability_text)))

# product_description
description_tag = soup.find("div", id="product_description")
product_description = description_tag.find_next_sibling("p").text.strip() if description_tag else ""

# category
breadcrumb = soup.find("ul", class_="breadcrumb")
category = breadcrumb.find_all("li")[2].a.text.strip()

# review_rating
rating_tag = soup.find("p", class_="star-rating")
rating_class = rating_tag.get("class", [])
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
review_rating = rating_map.get(next((cls for cls in rating_class if cls != "star-rating"), ""), 0)

# image_url
image_tag = soup.find("div", class_="item active").img
image_url = urljoin(url, image_tag["src"])

# Affichage des résultats
print(f"product_page_url: {product_page_url}")
print(f"universal_product_code (upc): {upc}")
print(f"title: {title}")
print(f"price_including_tax: {price_including_tax}")
print(f"price_excluding_tax: {price_excluding_tax}")
print(f"number_available: {number_available}")
print(f"product_description: {product_description}")
print(f"category: {category}")
print(f"review_rating: {review_rating}")
print(f"image_url: {image_url}")
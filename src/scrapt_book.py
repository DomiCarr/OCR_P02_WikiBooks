#----------------------------------------------------------------------
# scrapt_book.py
#
# App that extract books information from the web site: https://books.toscrape.com/index.html
# ---------------------------------------------------------------------

# Standard library imports - built-in modules that come with Python
import csv
import os
import re
import sys
from urllib.parse import urljoin, urlparse

# External libraries installed via pip
import requests
from bs4 import BeautifulSoup

# Local Librairies : project-specific modules
from data_cleaner import clean_number, clean_repository_name
from log_config import logger
from requests_tools import make_requests

# ---------------------------------------------------------------
# Function that opens the CSV file and writes the header row.
# ---------------------------------------------------------------

def write_csv_header(csv_path):
    """
    Function that opens the CSV file and writes the header row.

    Parameters
    IN: csv path (str) : Path to the csv file
    OUT: none
    """
    csv_header = [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product description",
        "category",
        "review_rating",
        "image url"
        ]

    try:
        with open(csv_path, "w", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(csv_header)
    except IOError as e:
        logger.info(f"Erreur writing CVS header to {csv_path: {e}}")

# ---------------------------------------------------------------
# Function that download the book image
# ---------------------------------------------------------------

def download_book_image(book_title, product_page_url, image_url, image_dir):
    # Clean the title: replace all non-alphanumeric characters with an underscore
    clean_title = re.sub(r'[^a-zA-Z0-9]+', '_', book_title.strip().lower())
    
    # Replace multiple consecutive underscores with a single underscore
    clean_title = re.sub(r'_+', '_', clean_title)
    
    # Remove underscores at the start or end of the string
    clean_title = clean_title.strip('_')

    # Extract book ID from the URL
    match = re.search(r'_(\d+)/index\.html$', product_page_url)
    book_id = match.group(1) if match else "unknown"

    # Get the image file extension
    image_ext = os.path.splitext(urlparse(image_url).path)[1]

    # Construct the final image filename
    image_filename = f"{clean_title}_{book_id}{image_ext}"
    image_path = os.path.join(image_dir, image_filename)

    # Request image_url; return None if the request fails
    if (response := make_requests(image_url)) is None:
        return

    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        raise ConnectionError(f"Failed to download image: {response.status_code}")

# ---------------------------------------------------------------
# Function that writes a book row to the CSV file
# ---------------------------------------------------------------

def write_book_line(product_page_url, image_dir):

    # Request product_page_url; return None if the request fails
    if (response := make_requests(product_page_url)) is None:
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # ==== Scrap === >> book title
    title_soup = soup.find('h1')
    if title_soup:
        title = title_soup.text.strip()
    else:
        title = "NA"
        logger.warning(f"Title not found on page: {product_page_url}")


    # ==== Scrap === >> product informations from the product information table
    tds_soup = soup.find_all('td')

    if len(tds_soup) > 6:

        # 1st td: upc code
        universal_product_code = tds_soup[0].text.strip()

    # 3rd td: price including taxes
        price_including_tax = clean_number(tds_soup[2].text.strip())

        # 4th td : price excluding taxes
        price_excluding_tax = clean_number(tds_soup[3].text.strip())

        # 5th td: number of available books
        number_available = clean_number(tds_soup[5].text.strip())
    else:
        # Default values or error handling if there are not enough <td> elements
        universal_product_code = "NA"
        price_including_tax = 0.0
        price_excluding_tax = 0.0
        number_available = 0
        logger.warning(f"Not enough <td> elements found on page: {product_page_url}")

    # ==== Scrap === >> product_description
    description_soup = soup.find('div', id='product_description')
    if description_soup:
        description_soup_sibling = description_soup.find_next_sibling('p')
        if description_soup_sibling:
            product_description = description_soup_sibling.text.strip()
        else:
            product_description = "NA"
            logger.warning(f"Product description paragraph not found on page: {product_page_url}")
    else:
        product_description = "NA"
        logger.warning(f"Product description block not found on page: {product_page_url}")

    # ==== Scrap === >> Category from breadcrumb navigation
    breadcrumb_soup = soup.find("ul", class_="breadcrumb")

    if breadcrumb_soup:
        breadcrumb_soup_links = breadcrumb_soup.find_all("a")
        if breadcrumb_soup_links:
            category = breadcrumb_soup_links[2].text.strip()
        else:
            category = "NA"
            logger.warning(f"Category link not found in breadcrumb on page: {product_page_url}")
    else:
        category = "NA"
        logger.warning(f"Breadcrumb not found on page: {product_page_url}")

    # ==== Scrap === >> rating 

    # Find the <p> tag with class "star-rating"
    rating_soup = soup.find("p", class_="star-rating")

    if rating_soup:
        # Get the list of classes from the tag; default to empty list if none
        rating_soup_classes = rating_soup.get("class", [])

        if rating_soup_classes and len(rating_soup_classes) > 1:
            # The second class indicates the rating as a word ("One", "Two", ...)
            rating_text = rating_soup_classes[1]

            # Map rating text to numeric value using match-case (Python 3.10+)
            match rating_text:
                case 'One':
                    rating = 1
                case 'Two':
                    rating = 2
                case 'Three':
                    rating = 3
                case 'Four':
                    rating = 4
                case 'Five':
                    rating = 5
                case _:
                    rating = 0  # Default if unknown rating text
        else:
            rating = 0
            logger.warning(f"Rating class missing or incomplete on page: {product_page_url}")
    else:
        rating = 0
        logger.warning(f"Rating element not found on page: {product_page_url}")

    # ==== Scrap === >> image extraction and download

    # Find the <img> tag inside the <div class="item active">
    image_container_soup = soup.find("div", class_="item active")

    if image_container_soup:
        image_soup = image_container_soup.find("img")

        if image_soup and image_soup.get("src"):
            # build image URL 
            image_url = urljoin(product_page_url, image_soup.get("src"))

            # Download image using helper function
            download_book_image(title, product_page_url, image_url, image_dir)
        else:
            image_url = "NA"
            logger.warning(f"Image tag or src attribute missing on page: {product_page_url}")
    else:
        image_url = "NA"
        logger.warning(f"Image container <div class='item active'> not found on page: {product_page_url}")


    # write the book row in the cvs file
    ligne = [
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        rating,
        image_url
        ]
    
    CSV_PATH_FILE = "../data/output/wikibooks.csv"
    try:
        # Open CSV file in append mode with UTF-8 encoding to support special characters
        with open(CSV_PATH_FILE, "a", newline="") as fichier_csv:
            # Write the book row
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(ligne)
    except Exception as e:
        logger.error(f"Error writing to CSV file {CSV_PATH_FILE}: {e}") # Log error on CSV write failure

    #-------------------------------------------------------------------
    #TEST LINES FOR ONE BOOK - TO BE DELETED OR DISABLED
    #-------------------------------------------------------------------
    #logger.info(f"product_page_url: {product_page_url}")
    #logger.info(f"universal_product_code: {universal_product_code}")
    #logger.info(f"title: {title}")
    #logger.info(f"price_including_tax: {price_including_tax}")
    #logger.info(f"price_excluding_tax: {price_excluding_tax}")
    #logger.info(f"number_available: {number_available}")
    #logger.info(f"product description: {product_description}")
    #logger.info(f"category: {category}")
    #logger.info(f"review_rating: {rating}")
    #logger.info(f"image url: {image_url}")    
    
    #sys.exit()

# ---------------------------------------------------------------
# Function that retrieves all books from a category
# and writes them to the CSV file.
# ---------------------------------------------------------------

def extract_books_categorie(url_categ, image_dir):

    # Request url_categ; return None if the request fails
    if (response := make_requests(url_categ)) is None:
        return

    # Check if the HTTP response status is ok (200-299)
    if not response.ok:
        logger.warning(f"Request failed for category page: {url_categ} with status code {response.status_code}")
        return  # Exit the function if the request failed

    soup = BeautifulSoup(response.content, "html.parser")

    book_urls = []
    for h3 in soup.find_all("h3"):
        href = h3.find("a")
        if href and href.has_attr("href"):
            href_url = href["href"]
            full_url = urljoin(url_categ, href_url)
            book_urls.append(full_url)
        else:
            logger.warning(f"'a' tag with href not found in h3 on page: {url_categ}")

    for book_url in book_urls:
        write_book_line(book_url, image_dir)

    #-------------------------------------------------------------------
    #TEST LINES FOR ONE CATEGORY - TO BE DELETED OR DISABLED
    #-------------------------------------------------------------------
    #sys.exit()

# ---------------------------------------------------------------
# Function that extract all categories
# and writes the books from each category to the CSV file
# ---------------------------------------------------------------

def extract_categories():
    url_index = "https://books.toscrape.com/index.html"
    response = requests.get(url_index)
    soup = BeautifulSoup(response.content, "html.parser")

# <aside> block containing the list of all book categories
    category_bloc_soup = soup.find("aside", class_="sidebar")
    categories_li = category_bloc_soup.find_all("li")
    for li in categories_li[1:]:

        href = li.find("a")

        # Extract and normalize category name
        category_name_raw = href.text.strip()
        category_name = clean_repository_name(category_name_raw)
        logger.info(f"=====> CATEGORY NAME: {category_name}")
        print(f"=====> CATEGORY NAME: {category_name}")

        # Build local image directory path
        image_dir = os.path.join("..","data", "output", "images", category_name)
        os.makedirs(image_dir, exist_ok=True)

        # Build full category URL
        url_categ = href["href"]
        full_url = urljoin(url_index, url_categ)

        # Scrape all books in category
        extract_books_categorie(full_url, image_dir)

# ---------------------------------------------------------------
# main 
# ---------------------------------------------------------------

csv_path = "../data/output/wikibooks.csv"  

def main():
    logger.info("========== >>>> Program started")
    write_csv_header(csv_path)
    extract_categories()
    logger.info("<<<< =========== Program ended")

if __name__ == "__main__":
    main()



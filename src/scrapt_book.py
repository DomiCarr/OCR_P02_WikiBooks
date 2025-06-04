import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from data_cleaner import clean_number
import re
import sys

# ---------------------------------------------------------------
# Function that opens the CSV file and writes the header row.
# ---------------------------------------------------------------

def write_csv_header():
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

    with open("../data/output/wikibooks.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(csv_header)

# ---------------------------------------------------------------
# Function that download the book image
# ---------------------------------------------------------------

# def download_book_image(book_title, image_url, image_dir):
def download_book_image(book_title, product_page_url, image_url, image_dir):
    title_clean = re.sub(r"[^\w\-]+", "_", book_title.lower())
    print ("title_clean: ", title_clean)
    print('product_page_url: ',product_page_url)
    print ("image_url: ", product_page_url)
    print ("image_dir: ", image_dir)
    

# ---------------------------------------------------------------
# Function that writes a book row to the CSV file
# ---------------------------------------------------------------

def write_book_line(url_book):

    url = url_book

    # url de la page du livre
    product_page_url = url

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        # book title
        title = soup.find('h1').text

        # on extrait la table
        table = soup.find('table')
        tds = soup.find_all('td')

        # upc code
        universal_product_code = tds[0].text

        # price including taxes
        price_including_tax = clean_number(tds[2].text)

        # price excluding taxes
        price_excluding_tax = clean_number(tds[3].text)

        # number of available books
        number_available = clean_number(tds[5].text)

        # product_description
        div_description = soup.find('div', id='product_description')
        product_description = div_description.find_next_sibling('p').text.strip() 

        # category
        categ_bloc = soup.find_all('a')
        category = categ_bloc[3].text

        # rating
        rating_tag = soup.find("p", class_="star-rating")
        rating_text = rating_tag.get("class")[1]  
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
                rating = 0  # Valeur par défaut si inconnu

        # image url
        bloc_image = soup.find("div", class_="item active").img
        image_url = urljoin(url,bloc_image["src"])
        image_dir = "data/output/images"

        # downlaod image 
        download_book_image(title, product_page_url, image_url, image_dir) 

    # csv book row
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

    with open("../data/output/wikibooks.csv", "a", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(ligne)

    """
    print('product_page_url: ',product_page_url)
    print('universal_product_code: ',universal_product_code)
    print('title: ', title)
    print('price_including_tax: ',price_including_tax) 
    print('price_excluding_tax: ',price_excluding_tax)
    print('number_available: ',number_available) 
    print('product description: ',product_description) 
    print('category: ', category)
    print('review_rating: ',rating) 
    print('image url: ',image_url)     
    """

# ---------------------------------------------------------------
# Function that retrieves all books from a category
# and writes them to the CSV file.
# ---------------------------------------------------------------

def extract_books_categorie(url_categ):
    response = requests.get(url_categ)
    soup = BeautifulSoup(response.content, "html.parser")

    book_urls = []
    for h3 in soup.find_all("h3"):
        href = h3.find("a")
        href_url = href["href"]
        full_url = urljoin(url_categ, href_url)
        book_urls.append(full_url)

    for book_url in book_urls:
        write_book_line(book_url)

    # TEST LINE TO BE DELETED OR COMMENTED
        print("End of scrapping book page")
        sys.exit()

# ---------------------------------------------------------------
# Function that extract all categories
# and writes the books from each category to the CSV file
# ---------------------------------------------------------------

def extract_categories():
    url_index = "https://books.toscrape.com/index.html"
    response = requests.get(url_index)
    soup = BeautifulSoup(response.content, "html.parser")

# bloc_aside des categories
    bloc_aside = soup.find("aside", class_="sidebar")
    for li in bloc_aside.find_all("li"):
        href = li.find("a")
        url_categ = href["href"]
        full_url = urljoin(url_index, url_categ)
        extract_books_categorie(full_url)
        print(url_categ)

# TEST LINE TO BE DELETED OR COMMENTED
#        print("End of scrapping books category")
#        sys.exit()

    

# ---------------------------------------------------------------
# main 
# ---------------------------------------------------------------

def main():
    write_csv_header()
    extract_categories()

if __name__ == "__main__":
    main()

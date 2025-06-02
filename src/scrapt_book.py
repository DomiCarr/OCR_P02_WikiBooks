import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# ---------------------------------------------------------------
# Fonction qui ouvre le fichier csv et ecrit écrit la ligne entete
# ---------------------------------------------------------------

def ecrit_entete():
    en_tete = [
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
        writer.writerow(en_tete)

# ---------------------------------------------------------------
# Fonction qui écrit la ligne d'un livre dans le fichier csv
# ---------------------------------------------------------------

def ecrit_ligne(url_book):

    url = url_book

    # url de la page du livre
    product_page_url = url


    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        # titre du livre
        title = soup.find('h1').text

        # on extrait la table
        table = soup.find('table')
        tds = soup.find_all('td')

        # code upc
        universal_product_code = tds[0].text

        # prix avec les taxes
        price_including_tax = tds[2].text

        # prix sans les taxes
        price_excluding_tax = tds[3].text

        # nombre d'ouvrages disponibles
        number_available = tds[5].text

        # product_description
        div_description = soup.find("div", id="product_description")
        product_description = div_description.find_next_sibling("p").text.strip() 

        # category
        categ_bloc = soup.find_all('a')
        category = categ_bloc[3].text


        # rating
        rating_tag = soup.find("p", class_="star-rating")
        rating = rating_tag.get("class")[1]  

        # image url
        bloc_image = soup.find("div", class_="item active").img
        image_url = urljoin(url,bloc_image["src"])




    # ligne du fichier csv
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
        writer

"""
    print('product_page_url: ',product_page_url)
    print('universal_product_code: ',universal_product_code)
    print('title: ', title)
    print('price_including_tax: ',price_including_tax) 
    print('price_excluding_tax: ',price_excluding_tax)
    print('number_available: ',number_available) 
    print('product description: ',description) 
    print('category: ', category)
    print('review_rating: ',rating) 
    print('image url: ',image_url)     
"""

# ---------------------------------------------------------------
# Fonction qui recupère tous les livres d'une categorie 
# pour les ecrire dans le fichier csv
# ---------------------------------------------------------------

def recupere_books_categorie(url_categ):
    response = requests.get(url_categ)
    soup = BeautifulSoup(response.content, "html.parser")

    book_urls = []
    for h3 in soup.find_all("h3"):
        href = h3.find("a")
        href_url = href["href"]
        full_url = urljoin(url_categ, href_url)
        book_urls.append(full_url)

    for book_url in book_urls:
        ecrit_ligne(book_url)


# ---------------------------------------------------------------
# Fonction qui récupère toutes les catégories 
# et ecrit les livres de chaque categorie dans le fichier csv
# ---------------------------------------------------------------

def recupere_categories():
    url_categ = "https://books.toscrape.com/index.html"
    response = requests.get(url_categ)
    soup = BeautifulSoup(response.content, "html.parser")

# bloc_aside des categories
    bloc_aside = soup.find("aside", class_="sidebar")
    for li in bloc_aside.find_all("li"):
        href = li.find("a")
        href_url = href["href"]
        full_url = urljoin(url_categ, href_url)
        recupere_books_categorie(full_url)

        


# ---------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------

# IF MAIN


def main():
    ecrit_entete()
    recupere_categories()

if __name__ == "__main__":
    main()
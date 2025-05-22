import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

# url de la page du livre
product_page_url = url
print('product_page_url: ',product_page_url)


response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')

#   titre du livre
    title = soup.find('h1').text
    print('title: ', title)


    table = soup.find('table')
    print('table: ', table)

#   on extrait la table
    tds = soup.find_all('td')

#   code upc
    universal_product_code = tds[0].text
#   prix avec les taxes
    price_including_tax = tds[2].text
#   prix sans les taxes
    price_excluding_tax = tds[3].text
#   nombre d'ouvrages disponibles
    number_available = tds[5].text

    print('universal_product_code: ',universal_product_code)
    print('price_including_tax: ',price_including_tax) 
    print('price_excluding_tax: ',price_excluding_tax)
    print('number_available: ',number_available) 

    categ_bloc = soup.find_all('a')
    category = categ_bloc[3].text
    print ("category: ", category)

    rating_bloc = soup.find_all('p')
    print('rating_bloc:', rating_bloc)

#    rating = rating_bloc[3].text
#    print ("rating: ", rating)






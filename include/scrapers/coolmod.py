import logging
from .core.interface import Product
from .core.http import HttpScraper
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Coolmod(HttpScraper):
    def extract_data(self, url:str) -> Product:
        html_content = super()._get_html(url)
        html_soup = BeautifulSoup(html_content,"lxml")

        #Get price
        price_span = html_soup.find("span", class_= "product_price int_price")
        price = float(price_span.get_text(strip=True).replace(".",""))

        #Get currency
        currency = html_soup.find("span", class_="currency_symbol")
        currency = currency.get_text(strip=True)

        #Get name
        name_span = html_soup.find("h1", class_="text-2xl font-bold")
        name = str(name_span.get_text(strip=True))
        name = super()._normalize_text(name)

        #Get timestamp
        timestamp = datetime.now()

        #Create Product object
        product = Product(
            name=name,
            price=price,
            currency=currency,
            url=url,
            timestamp=timestamp)
        return product
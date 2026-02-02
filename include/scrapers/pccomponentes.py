import logging
from .core.interface import Product
from .core.http import HttpScraper
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PcComponentes(HttpScraper):
    def extract_data(self, url:str) -> Product:
        html_content = super()._get_html(url)
        html_soup = BeautifulSoup(html_content,"lxml")

        #Get price and currency
        price_span = html_soup.select_one("#pdp-price-current-integer")
        price_w_currency  = price_span.get_text(strip=True)

        price = price_w_currency[:-1].replace(".","")
        price = float(price.replace(",","."))
        currency = price_w_currency[-1]

        #Get name
        name_span = html_soup.select_one("#pdp-title")
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
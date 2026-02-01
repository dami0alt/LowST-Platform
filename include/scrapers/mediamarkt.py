import logging
from .base_scraper import Product,ScraperBase
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaMarkt(ScraperBase):
    def extract_data(self, url:str) -> Product:
        html_content = super()._get_html(url)
        html_soup = BeautifulSoup(html_content,"lxml")

        #Get price
        price_span = html_soup.find("span", {"data-test": "branded-price-whole-value"})
        price = float(price_span.get_text(strip=True).replace(",",""))

        #Get currency
        currency = html_soup.find("span", {"data-test": "branded-price-currency"})
        currency = currency.get_text(strip=True)[-1]

        #Get name
        name_span = html_soup.find("h1", class_="sc-94eb08bc-0 dPxwlD")
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
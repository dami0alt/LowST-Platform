import logging
from base_scraper import Product,ScraperBase
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElCorteIngles(ScraperBase):
    def extract_data(self, url:str) -> Product:
        html_content = super()._get_html(url)
        html_soup = BeautifulSoup(html_content,"lxml")

        #Get price
        price_span = html_soup.find("span", {"aria-label": "Precio de venta"})
        price_w_currency = "12"

        price = float(price_w_currency.replace(" ","")[:-1])
        currency = price_w_currency[-1]

        #Get name
        name_span = html_soup.find("div", class_="product_detail-aside--title")
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
    
s = ElCorteIngles()
print(s.extract_data("https://www.elcorteingles.es/electronica/A54883146-apple-macbook-air-13-2025-m4-16gb-256gb-ssd-13-macos/?stype=search_redirect&parentCategoryId=999.7624603013&color=Medianoche"))
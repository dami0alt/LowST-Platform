import logging
from .core.interface import Product
from .core.http import HttpScraper
from bs4 import BeautifulSoup
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PcComponentes(HttpScraper):
    def extract_data(self, url:str) -> Product:
        gtin13 = None
        name = None
        manufacturer = None
        price = None
        currency = None
        
        # Get html and parse to soup
        html_content = super()._get_html(url)
        html_soup = BeautifulSoup(html_content,"lxml")

        # Find alls LD+JSON
        scripts = html_soup.find_all("script", {"type": "application/ld+json"})

        # Get GTIN13(EAN) & Manufacturer
        if scripts:
            for script in scripts:
                try:
                    data = json.loads(script.string)

                    if isinstance(data, dict):
                        if data.get("@type","").lower() == "product":
                            gtin13 = int(data["gtin13"])
                            brand = data.get("brand")
                            if isinstance(brand, dict):
                                manufacturer = brand.get("name",None).capitalize()
                            break
                except json.JSONDecodeError:
                    continue
        
        # Get price and currency
        price_span = html_soup.select_one("#pdp-price-current-integer")

        if price_span:
            price_w_currency  = price_span.get_text(strip=True)
    
            price = price_w_currency[:-1].replace(".","")
            price = float(price.replace(",","."))
            currency = price_w_currency[-1]

        # Get name
        name_span = html_soup.select_one("#pdp-title")
        if name_span:
            name = str(name_span.get_text(strip=True))
            name = super()._normalize_text(name)

        #Get timestamp
        timestamp = datetime.now()

        #Create Product object
        product = Product(
            ean=gtin13,
            name=name,
            manufacturer=manufacturer,
            price=price,
            currency=currency,
            url=url,
            timestamp=timestamp,
            source="PcComponentes"
        )
        return product
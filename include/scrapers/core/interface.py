import logging
from datetime import datetime 
import unicodedata
import re
from dataclasses import dataclass 
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Product():
    name: str  
    price: float
    currency: str
    url: str
    timestamp: datetime

class ScraperBase(ABC):
    @abstractmethod  
    def extract_data(self, url:str) -> Product:
        pass
    
    def _normalize_text(self, text:str) -> str:
        text = text.replace('""', '"').replace('"', '')
        text = text.replace(",", " -")

        text = text.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text)
        text = unicodedata.normalize("NFKD", text)

        text = "".join(c for c in text if not unicodedata.combining(c))
        text = " ".join(text.split())
        
        return text.strip()

        
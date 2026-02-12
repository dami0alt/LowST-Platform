import logging
from datetime import datetime 
import unicodedata
import re
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Product():
    # primary keys
    link_id: int
    timestamp: datetime
    # obligatory fields
    name: str  
    price: float
    currency: str = "EUR"
    # optional fields
    manufacturer: Optional[str] = None
    ean: Optional[str] =  None
    is_refurbished: bool = False
    store_amount: int = -1
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

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

        
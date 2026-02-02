from .interface import ScraperBase
import logging
from curl_cffi import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserScraper(ScraperBase):
    def _get_html(self, url:str, impersonate:str ="chrome"):
        try:
            logger.warning(f"getting html from {url}")
            r = requests.get(
                url,
                impersonate=impersonate
            )
            r.raise_for_status()
            return r.text 
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting html from {url}:{e}")
            return None
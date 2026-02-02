import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from include.scrapers.pccomponentes import PcComponentes
import logging
import coloredlogs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("testing")
coloredlogs.install(level="INFO",logger=logger)

url = "https://www.pccomponentes.com/apple-iphone-17-pro-max-256gb-azul-oscuro"

def test_engines():
    
    logger.info("Testing PcComponentes (HTTP)...")
    scraper = PcComponentes()
    product = scraper.extract_data(url)
    if product and product.price > 0:
        logger.info("PcComponentes: APPROVE !!")
    else:
        logger.error("PcComponentes: FAILED (Provable blocked)")

if __name__ == "__main__":
    test_engines()
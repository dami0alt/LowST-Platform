import logging
import yaml
import time
import random
import coloredlogs
from include.scrapers.pccomponentes import PcComponentes
from include.scrapers.mediamarkt import MediaMarkt
from include.scrapers.coolmod import Coolmod
from include.db_handler import DBHandler
from duckdb import Error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO",logger=logger)

data_wh_path = "./data/duckdb_wh.db"

PcComponentes_Scraper = PcComponentes()
MediaMarkt_Scraper = MediaMarkt()
Coolmod_Scraper = Coolmod()

Db_Handler = None
try:
    with open("./configs/targets.yaml","r",encoding="utf-8") as f:
        config = yaml.safe_load(f)
    Db_Handler = DBHandler(data_wh_path)
    for target in config["targets"]:
        target_name = target["target"]
        items_counter = 0
        errors_counter = 0
        for item in target["products"]:
            product = None
            source = ""
            try:
                match target_name:
                    case "PcComponentes":
                        product = PcComponentes_Scraper.extract_data(item["url"])
                        source = "PcComponentes"
                    case "MediaMarkt":
                        product = MediaMarkt_Scraper.extract_data(item["url"])
                        source = "MediaMarkt"
                    case "Coolmod":
                        product = Coolmod_Scraper.extract_data(item["url"])
                        source = "Coolmod"
                if product:
                    Db_Handler.insert_product(product=product,source=source)
                items_counter +=1
            except Exception as ex:
                errors_counter +=1
                logger.error(f"{item['name']} from {target_name} coludn't be processed: {ex}")

            n = random.randint(1, 3)
            time.sleep(n)
        logger.info(f"Products from {target_name} inserted. items: {items_counter}, errors: {errors_counter}")
    Db_Handler.show_table()
except Error as er:
    logger.error(f"Data base error rised: {er}")
except Exception as ex:
    logger.error(f"Generic error rised:{ex}")
finally:
    if Db_Handler:
        Db_Handler.close_connection()


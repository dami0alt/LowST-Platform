import logging
import os
import yaml
import time
import random
from dataclasses import asdict
import pandas as pd
from include.scrapers.pccomponentes import PcComponentes
from include.scrapers.mediamarkt import MediaMarkt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_dir = "./data"

PcComponentes_Scraper = PcComponentes()
MediaMarkt_Scraper = MediaMarkt()

with open("./configs/targets.yaml","r",encoding="utf-8") as f:
    config = yaml.safe_load(f)

for target in config["targets"]:
    target_dir = f"{data_dir}/{target['target']}"
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    for item in target["products"]:
        csv_path = f"{target_dir}/products_history.csv"
        match target['target']:
            case "PcComponentes":
                product = PcComponentes_Scraper.extract_data(item["url"])
            case "MediaMarkt":
                product = MediaMarkt_Scraper.extract_data(item["url"])
       
        if product:
            df = pd.DataFrame([asdict(product)])
            if not os.path.exists(csv_path):
                df.to_csv(csv_path,index=False,)
            else:
                df.to_csv(csv_path, mode="a",index=False, header=False)
        n = random.randint(1, 3)
        time.sleep(n)


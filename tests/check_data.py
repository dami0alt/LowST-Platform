import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from include.db_handler import DBHandler
import coloredlogs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("testing")
coloredlogs.install(level="INFO",logger=logger)

data_root_dir = "./data/duckdb_wh.db"
Db_Handler = DBHandler(data_root_dir)

Db_Handler.show_table()
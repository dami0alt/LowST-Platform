import logging
import duckdb
import os
from include.scrapers.core.interface import Product 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBHandler():
    def __init__(self, db_path:str):
        self._db_dir_path = os.path.dirname(db_path)
        self._db_path = db_path
        self._schema = "BRONZE"
        self._table = "PRODUCTS_HISTORY"

        if not os.path.exists(self._db_dir_path):
            os.makedirs(self._db_dir_path)

        logger.info("Connecting to data warehouse")
        self._con_db = duckdb.connect(self._db_path)

        self._check_structure_db()

    def show_table(self, table_name:str = None):
        con = self._con_db
        if table_name:
            con.table(table_name).show()
        else:
            con.table(self._schema+"."+self._table).show()

    def insert_product(self, product:Product, source:str):
        con = self._con_db
        schema = self._schema
        table = self._table

        con.execute(
             f"INSERT INTO {schema}.{table}(name, price, currency, url, timestamp, source) VALUES(?,?,?,?,?,?)",
             (product.name,product.price,product.currency,product.url,product.timestamp,source)
        )

    def delete_table(self, table_name:str = None):
        con = self._con_db
        response = input(f"Are you shure you want delete whole data in {self._schema+"."+self._table}: y/Y")
        if response.lower() == "y":
            if table_name:
                query = f"DELETE FROM {table_name}"
            else:
                query = f"DELETE FROM {self._schema+"."+self._table}"
            con.execute(query)
            logger.info("Table cleared")

        
    def close_connection(self):
        logger.warning("Connection closed")
        self._con_db.close()

    def _schema_exists(self,schema_name:str) -> bool:
        con = self._con_db
        query = """
        SELECT EXISTS(
            SELECT 1
            FROM information_schema.schemata
            WHERE schema_name = ?
        );
        """
        return con.execute(query, [schema_name]).fetchone()[0]
    def _table_exists(self,schema_name:str,table_name:str) -> bool:
        con = self._con_db
        query = """
            SELECT EXISTS(
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = ?
                AND table_name = ?
                );
        """
        return con.execute(query, (schema_name,table_name)).fetchone()[0]
    
    def _check_structure_db(self):
        con = self._con_db
        schema = self._schema
        table = self._table

        if not self._schema_exists(schema):
            logger.info(f"Creating schema '{schema}' into db")
            ## Creat schema if not exist
            con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")

        if not self._table_exists(schema,table):
            logger.info(f"Creating table '{schema}.{table}' into db")
            ## Creat table if not exist
            con.execute(f"""CREATE TABLE IF NOT EXISTS {schema}.{table}(
                    name VARCHAR,
                    price FLOAT,
                    currency VARCHAR,
                    url VARCHAR,
                    timestamp TIMESTAMP,
                    source VARCHAR
                );""")
        return con

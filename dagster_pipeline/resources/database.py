# Ce ficheir sert à declarer la base Duck DB impléménté 

import duckdb
from dagster import ConfigurableResource

class DuckDBResource(ConfigurableResource):
    database_path: str = "data/crypto.duckdb"

    def get_connection(self):
        return duckdb.connect(self.database_path)
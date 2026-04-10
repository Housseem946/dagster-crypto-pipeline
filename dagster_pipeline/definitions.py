from pathlib import Path
from dagster import Definitions
from dagster_dbt import DbtCliResource

from dagster_pipeline.assets.extract import raw_crypto_prices
from dagster_pipeline.assets.dbt_assets import crypto_dbt_assets
from dagster_pipeline.resources.database import DuckDBResource

DBT_PROJECT_DIR = Path(__file__).resolve().parents[1] / "dbt_project" / "crypto_pipeline"

defs = Definitions(
    assets=[raw_crypto_prices, crypto_dbt_assets],
    resources={
        "duckdb_resource": DuckDBResource(database_path="data/crypto.duckdb"),
        "dbt": DbtCliResource(project_dir=str(DBT_PROJECT_DIR)),
    },
)
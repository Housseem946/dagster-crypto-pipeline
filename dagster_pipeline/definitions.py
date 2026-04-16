from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_pipeline.assets.extract import raw_crypto_prices
from dagster_pipeline.assets.dbt_assets import crypto_dbt_assets, DBT_PROJECT_DIR
from dagster_pipeline.resources.database import DuckDBResource
from dagster_pipeline.jobs import crypto_pipeline_job
from dagster_pipeline.schedules import hourly_schedule
from dagster_pipeline.sensors import price_drop_sensor

defs = Definitions(
    assets=[raw_crypto_prices, crypto_dbt_assets],
    resources={
        "duckdb_resource": DuckDBResource(database_path="data/crypto.duckdb"),
        "dbt": DbtCliResource(project_dir=str(DBT_PROJECT_DIR))
    },
    jobs=[crypto_pipeline_job],
    schedules=[hourly_schedule],
    sensors=[price_drop_sensor]
)
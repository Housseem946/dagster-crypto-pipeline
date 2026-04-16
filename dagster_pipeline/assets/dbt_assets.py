from pathlib import Path
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

DBT_PROJECT_DIR = Path(__file__).resolve().parents[2] / "dbt_project" / "crypto_pipeline"

@dbt_assets(manifest=DBT_PROJECT_DIR / "target" / "manifest.json")
def crypto_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()




from dagster import define_asset_job, AssetSelection

# Job qui fait tourner tout le pipeline
crypto_pipeline_job = define_asset_job(
    name="crypto_pipeline_job",
    selection=AssetSelection.all(),
    description="Pipeline complet : extraction CoinGecko → DuckDB → dbt"
)
import requests
import pandas as pd
from dagster import asset, get_dagster_logger
from dagster_pipeline.resources.database import DuckDBResource


COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana,cardano,ripple",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False,
    "price_change_percentage": "24h,7d"
}

@asset(group_name="ingestion", compute_kind="python")
def raw_crypto_prices(duckdb_resource: DuckDBResource) -> None:
    """Fetch crypto prices from CoinGecko and store in DuckDB."""
    logger = get_dagster_logger()
    
    logger.info("Fetching data from CoinGecko...")
    response = requests.get(COINGECKO_URL, params=PARAMS)
    response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data)
    
    # Garder les colonnes utiles
    df = df[[
        "id", "symbol", "name", "current_price",
        "market_cap", "total_volume",
        "price_change_percentage_24h",
        "price_change_percentage_7d_in_currency",
        "last_updated"
    ]]
    
    df["fetched_at"] = pd.Timestamp.now()
    
    logger.info(f"Fetched {len(df)} coins")
    
    # Stocker dans DuckDB
    conn = duckdb_resource.get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_crypto_prices AS 
        SELECT * FROM df LIMIT 0
    """)
    conn.execute("INSERT INTO raw_crypto_prices SELECT * FROM df")
    conn.close()
    
    logger.info("Data stored in DuckDB ✓")
select
    id,
    symbol,
    name,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h,
    price_change_percentage_7d_in_currency,
    cast(last_updated as timestamp) as last_updated,
    cast(fetched_at as timestamp) as fetched_at
from raw_crypto_prices
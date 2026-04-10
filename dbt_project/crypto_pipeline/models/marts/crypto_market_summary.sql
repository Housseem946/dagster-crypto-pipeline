select
    name,
    symbol,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h,
    price_change_percentage_7d_in_currency,
    fetched_at
from {{ ref('stg_crypto_prices') }}
order by market_cap desc
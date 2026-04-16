import pytest
import pandas as pd

def make_sample_df():
    return pd.DataFrame([
        {
            "id": "bitcoin", "symbol": "btc", "name": "Bitcoin",
            "current_price": 70000, "market_cap": 1400000000000,
            "total_volume": 30000000000,
            "price_change_percentage_24h": 2.5,
            "price_change_percentage_7d_in_currency": 5.1,
            "last_updated": "2024-01-01T00:00:00Z",
            "fetched_at": pd.Timestamp.now()
        },
        {
            "id": "ethereum", "symbol": "eth", "name": "Ethereum",
            "current_price": 3500, "market_cap": 420000000000,
            "total_volume": 15000000000,
            "price_change_percentage_24h": -1.2,
            "price_change_percentage_7d_in_currency": 3.0,
            "last_updated": "2024-01-01T00:00:00Z",
            "fetched_at": pd.Timestamp.now()
        }
    ])

def transform_staging(df):
    """Simule la logique de stg_crypto_prices."""
    df = df[[
        "id", "symbol", "name", "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h",
        "price_change_percentage_7d_in_currency",
        "last_updated", "fetched_at"
    ]].copy()
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])
    return df

def transform_marts(df):
    """Simule la logique de crypto_market_summary."""
    return df.sort_values("market_cap", ascending=False).reset_index(drop=True)

def test_staging_has_all_columns():
    """Vérifie que le staging garde toutes les colonnes."""
    df = transform_staging(make_sample_df())
    assert "current_price" in df.columns
    assert "market_cap" in df.columns
    assert "price_change_percentage_24h" in df.columns

def test_staging_datetime_cast():
    """Vérifie que last_updated est bien converti en datetime."""
    df = transform_staging(make_sample_df())
    assert pd.api.types.is_datetime64_any_dtype(df["last_updated"])

def test_staging_no_nulls_on_critical_columns():
    """Vérifie l'absence de nulls sur les colonnes clés."""
    df = transform_staging(make_sample_df())
    for col in ["id", "name", "current_price", "market_cap"]:
        assert df[col].isnull().sum() == 0, f"Null trouvé dans {col}"

def test_marts_sorted_by_market_cap():
    """Vérifie que le mart est trié par market cap décroissant."""
    df = transform_marts(transform_staging(make_sample_df()))
    caps = df["market_cap"].tolist()
    assert caps == sorted(caps, reverse=True)

def test_marts_no_duplicates():
    """Vérifie l'absence de doublons sur l'id."""
    df = transform_marts(transform_staging(make_sample_df()))
    assert df["id"].duplicated().sum() == 0

def test_price_drop_detection():
    """Vérifie la logique du sensor : détection de chute > 5%."""
    df = make_sample_df()
    threshold = -5.0
    drops = df[df["price_change_percentage_24h"] < threshold]
    assert len(drops) == 0  # aucune chute dans nos données mock

def test_price_drop_detection_triggered():
    """Vérifie que le sensor détecte bien une vraie chute."""
    df = make_sample_df()
    df.loc[0, "price_change_percentage_24h"] = -8.5
    threshold = -5.0
    drops = df[df["price_change_percentage_24h"] < threshold]
    assert len(drops) == 1
    assert drops.iloc[0]["name"] == "Bitcoin"
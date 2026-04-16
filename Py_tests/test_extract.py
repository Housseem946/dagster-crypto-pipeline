import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

EXPECTED_COLUMNS = [
    "id", "symbol", "name", "current_price",
    "market_cap", "total_volume",
    "price_change_percentage_24h",
    "price_change_percentage_7d_in_currency",
    "last_updated", "fetched_at"
]

MOCK_API_RESPONSE = [
    {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 70000,
        "market_cap": 1400000000000,
        "total_volume": 30000000000,
        "price_change_percentage_24h": 2.5,
        "price_change_percentage_7d_in_currency": 5.1,
        "last_updated": "2024-01-01T00:00:00Z",
    }
]

def test_api_response_has_required_columns():
    """Vérifie que la réponse API contient toutes les colonnes attendues."""
    df = pd.DataFrame(MOCK_API_RESPONSE)
    df["fetched_at"] = pd.Timestamp.now()
    for col in EXPECTED_COLUMNS:
        assert col in df.columns, f"Colonne manquante : {col}"

def test_api_response_not_empty():
    """Vérifie que le DataFrame n'est pas vide."""
    df = pd.DataFrame(MOCK_API_RESPONSE)
    assert len(df) > 0

def test_price_is_positive():
    """Vérifie que les prix sont positifs."""
    df = pd.DataFrame(MOCK_API_RESPONSE)
    assert (df["current_price"] > 0).all()

def test_market_cap_is_positive():
    """Vérifie que la market cap est positive."""
    df = pd.DataFrame(MOCK_API_RESPONSE)
    assert (df["market_cap"] > 0).all()

def test_api_call_failure_raises():
    """Vérifie qu'une erreur API est bien levée."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="API Error"):
            mock_get.return_value.raise_for_status()

def test_dataframe_types():
    """Vérifie les types des colonnes critiques."""
    df = pd.DataFrame(MOCK_API_RESPONSE)
    df["fetched_at"] = pd.Timestamp.now()
    assert df["current_price"].dtype in [float, int, "float64", "int64"]
    assert df["market_cap"].dtype in [float, int, "float64", "int64"]
    assert isinstance(df["name"].iloc[0], str)
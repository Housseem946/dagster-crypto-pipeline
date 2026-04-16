import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DB_PATH = "data/crypto.duckdb"

st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)

@st.cache_data(ttl=300)
def load_data():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT * FROM crypto_market_summary").df()
    conn.close()
    return df

@st.cache_data(ttl=300)
def load_history():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT name, current_price, fetched_at 
        FROM raw_crypto_prices 
        ORDER BY fetched_at ASC
    """).df()
    conn.close()
    return df

# --- Header ---
st.title("📈 Crypto Market Dashboard")
st.caption("Données en temps réel via CoinGecko • Orchestré par Dagster + dbt")

# --- Load data ---
try:
    df = load_data()
    history = load_history()
except Exception as e:
    st.error(f"Erreur de connexion à DuckDB : {e}")
    st.stop()

# --- KPI Cards ---
st.subheader("Vue d'ensemble du marché")
cols = st.columns(len(df))
for i, row in df.iterrows():
    delta_color = "normal" if row["price_change_percentage_24h"] >= 0 else "inverse"
    cols[i].metric(
        label=f"{row['name']} ({row['symbol'].upper()})",
        value=f"${row['current_price']:,.2f}",
        delta=f"{row['price_change_percentage_24h']:.2f}% (24h)"
    )

st.divider()

# --- Deux colonnes principales ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Market Cap")
    fig = px.bar(
        df, x="name", y="market_cap",
        color="name", text_auto=".2s",
        title="Market Capitalization (USD)"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Variation 24h vs 7j")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="24h %", x=df["name"],
        y=df["price_change_percentage_24h"],
        marker_color=["green" if v >= 0 else "red" 
                      for v in df["price_change_percentage_24h"]]
    ))
    fig2.add_trace(go.Bar(
        name="7j %", x=df["name"],
        y=df["price_change_percentage_7d_in_currency"],
        marker_color=["lightgreen" if v >= 0 else "salmon"
                      for v in df["price_change_percentage_7d_in_currency"]]
    ))
    fig2.update_layout(barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

# --- Évolution des prix ---
st.subheader("📉 Évolution des prix dans le temps")
coins = st.multiselect(
    "Sélectionne les cryptos",
    options=history["name"].unique(),
    default=list(history["name"].unique()[:3])
)
filtered = history[history["name"].isin(coins)]
fig3 = px.line(
    filtered, x="fetched_at", y="current_price",
    color="name", title="Prix historique (USD)"
)
st.plotly_chart(fig3, use_container_width=True)

# --- Table ---
st.subheader("📋 Données complètes")
st.dataframe(df, use_container_width=True)
from dagster import sensor, RunRequest, SkipReason, SensorEvaluationContext
from dagster_pipeline.jobs import crypto_pipeline_job
from dagster_pipeline.resources.database import DuckDBResource

PRICE_DROP_THRESHOLD = -5.0  # alerte si chute > 5%

@sensor(
    job=crypto_pipeline_job,
    name="price_drop_sensor",
    minimum_interval_seconds=3600,
    description="Déclenche une alerte si un coin chute de plus de 5%"
)
def price_drop_sensor(context: SensorEvaluationContext):
    conn = DuckDBResource(database_path="data/crypto.duckdb").get_connection()

    try:
        result = conn.execute("""
            SELECT name, price_change_percentage_24h
            FROM crypto_market_summary
            WHERE price_change_percentage_24h < ?
        """, [PRICE_DROP_THRESHOLD]).fetchall()
    except Exception:
        yield SkipReason("Table non disponible encore")
        return
    finally:
        conn.close()

    if not result:
        yield SkipReason("Aucune chute significative détectée")
        return

    coins = ", ".join([f"{row[0]} ({row[1]:.2f}%)" for row in result])
    context.log.warning(f"⚠️ Chute détectée : {coins}")

    yield RunRequest(
        run_key=str(context.cursor or "init"),
        tags={"alert": "price_drop", "coins": coins}
    )
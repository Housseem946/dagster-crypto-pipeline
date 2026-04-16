from dagster import ScheduleDefinition
from dagster_pipeline.jobs import crypto_pipeline_job

# Exécution toutes les heures
hourly_schedule = ScheduleDefinition(
    job=crypto_pipeline_job,
    cron_schedule="0 * * * *",
    name="hourly_crypto_schedule",
    description="Lance le pipeline crypto toutes les heures"
)
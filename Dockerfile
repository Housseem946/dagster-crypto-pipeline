FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p /app/data /app/.dagster

# Générer le manifest dbt
RUN cd dbt_project/crypto_pipeline && dbt compile --profiles-dir . && cd ../..

EXPOSE 3000 8501
# dagster-crypto-pipeline

Ce projet met en place un pipeline de données complet pour collecter, transformer et analyser des données de cryptomonnaies.
Il s’appuie sur un stack moderne de Data Engineering :

Dagster pour l’orchestration
dbt pour la transformation des données
DuckDB comme base analytique locale
Streamlit pour la visualisation

L’objectif est de construire une architecture simple, modulaire et industrialisable.


### Arboresence du projet 


```
dagster-crypto-pipeline/
│
├── dagster_pipeline/               # Package principal Dagster
│   ├── __init__.py
│   ├── definitions.py              # Point d'entrée Dagster
│   ├── jobs.py                     # Définition des jobs
│   ├── schedules.py                # Planification
│   ├── sensors.py                  # Déclencheurs événementiels
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── extract.py              # Extraction via API CoinGecko
│   │   └── dbt_assets.py           # Intégration des assets dbt
│   └── resources/
│       ├── __init__.py
│       └── database.py             # Connexion DuckDB
│
├── dbt_project/                   # Projet dbt
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_prices.sql      # Nettoyage des données brutes
│   │   └── marts/
│   │       ├── daily_summary.sql   # Agrégations journalières
│   │       └── moving_averages.sql # Calcul des moyennes mobiles
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── dashboard/
│   └── app.py                     # Application Streamlit
│
├── tests/                         # Tests unitaires (pytest)
│   ├── __init__.py
│   ├── test_extract.py
│   └── test_transforms.py
│
├── data/                          # Base DuckDB locale (ignorée par Git)
├── .env                           # Variables d'environnement
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Fonctionnement du pipeline

#### Extraction
- Récupération des données via l’API CoinGecko
- Stockage brut dans DuckDB

#### Transformation
- Modélisation des données avec dbt
- Séparation en couches :
    - staging : nettoyage
    - marts : agrégations métier
#### Orchestration
- Pipeline orchestré avec Dagster
- Possibilité de planification et de déclenchement automatique
#### Visualisation
- Dashboard interactif via Streamlit
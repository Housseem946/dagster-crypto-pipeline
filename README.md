# dagster-crypto-pipeline







### Arboresence du projet 
dagster-crypto-pipeline/
│
├── dagster_pipeline/               ← package principal Dagster
│   ├── __init__.py
│   ├── definitions.py              ← point d'entrée Dagster
│   ├── jobs.py                     ← définition des jobs
│   ├── schedules.py                ← planification
│   ├── sensors.py                  ← déclencheurs événementiels
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── extract.py              ← appel API CoinGecko
│   │   └── dbt_assets.py           ← assets dbt auto-générés
│   └── resources/
│       ├── __init__.py
│       └── database.py             ← connexion DuckDB
│
├── dbt_project/                    ← projet dbt
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_prices.sql      ← nettoyage raw
│   │   └── marts/
│   │       ├── daily_summary.sql   ← résumé journalier
│   │       └── moving_averages.sql ← moyennes mobiles
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── dashboard/
│   └── app.py                      ← Streamlit
│
├── tests/                          ← pytest
│   ├── __init__.py
│   ├── test_extract.py
│   └── test_transforms.py
│
├── data/                           ← fichier DuckDB local (gitignore)
├── .env                            ← variables d'environnement
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
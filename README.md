# Azure Weather Data Platform

Cloud data engineering project that ingests current weather observations from
OpenWeather and transforms them into Delta Lake tables on Azure Data Lake
Storage Gen2.

## Current Architecture

```text
OpenWeather API
      |
Azure Data Factory
      |-- reads the API secret from Azure Key Vault
      |-- writes JSON files to ADLS RAW
      `-- starts the Azure Databricks Job
                    |
                    `-- RAW -> Bronze -> Silver -> Gold
```

## Databricks Transformations — MVP 2

ADF starts the Databricks Job after all city files have been written to RAW.
The Job runs three dependent notebooks:

```text
databricks/bronze/raw_to_bronze.py
                |
                v
databricks/silver/bronze_to_silver.py
                |
                v
databricks/gold/silver_to_gold.py
```

Databricks accesses ADLS through the `dbc-weather-dev-yahia` managed identity,
the `weather_adls_credential` storage credential, and the `weather_datalake`
external location. No storage key is stored in the notebooks.

The transformations create these external Delta tables:

```text
weather.bronze.weather
weather.silver.weather
weather.gold.daily_city_weather
```

- Bronze preserves the OpenWeather payload and adds ingestion metadata.
- Silver flattens, types, validates, and deduplicates weather observations.
- Gold calculates daily weather indicators for each city.

The hourly ADF trigger is the only production schedule. Databricks does not
need a separate trigger because ADF starts the Job after ingestion succeeds.

## Security

- Local secrets are stored only in ignored `.env` files.
- Production secrets are stored in Azure Key Vault.
- Secrets are never committed to Git.
- Secrets are not stored in Terraform variables.
- ADF uses a system-assigned managed identity.
- Azure RBAC is used to grant the minimum required permissions.
- Public blob access is disabled.
- TLS 1.2 or later is required.

## Roadmap

1. **MVP 1 — Ingestion**
   - OpenWeather API
   - Azure Data Factory
   - Azure Key Vault
   - ADLS Gen2 RAW
   - Hourly trigger

2. **MVP 2 — Data Transformation**
   - Azure Databricks
   - PySpark
   - RAW → Bronze → Silver → Gold
   - Delta Lake

3. **MVP 3 — Analytics**
   - Azure SQL
   - Star schema
   - Power BI

4. **Industrialization**
   - Integration tests
   - Remote Terraform state
   - CI/CD
   - Monitoring and alerts
   - DEV / TEST / PROD environments
   - Architecture and operational documentation

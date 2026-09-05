# Azure Weather Data Platform

Cloud data engineering project that ingests current weather observations from
OpenWeather and transforms them into Delta Lake tables on Azure Data Lake
Storage Gen2.

```

## Project Demo

Watch the end-to-end Azure Weather Data Platform in action, including data
ingestion with Azure Data Factory and transformation with Azure Databricks.

[![Watch the Azure Weather Data Platform demo](https://img.youtube.com/vi/TL8enYKfsOQ/maxresdefault.jpg)](https://youtu.be/TL8enYKfsOQ)

**[Watch the full project demo on YouTube →](https://youtu.be/TL8enYKfsOQ)**

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

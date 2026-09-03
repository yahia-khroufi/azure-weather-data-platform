# Azure Weather Data Platform

Cloud data engineering project that ingests current weather observations from OpenWeather into Azure Data Lake Storage Gen2.

The first milestone focuses only on the RAW ingestion layer. Databricks, Azure SQL, and Power BI are introduced in later stages.

The hourly trigger should only be enabled after the pipeline successfully writes RAW weather files to ADLS.

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

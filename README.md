# Azure Weather Data Platform

Cloud data engineering project that ingests current weather observations from OpenWeather into Azure Data Lake Storage Gen2.

The first milestone focuses only on the RAW ingestion layer. Databricks, Azure SQL, and Power BI are introduced in later stages.

## Current Scope

```text
OpenWeather API
      |
Azure Data Factory
(system-assigned managed identity)
      |
      |-- reads secret --> Azure Key Vault
      |
      `-- writes RAW ----> ADLS Gen2
```

The repository currently provides:

- a local OpenWeather client for development and API contract testing;
- reusable configuration and initial data quality rules;
- Terraform infrastructure for the Resource Group, ADLS Gen2, Key Vault, ADF,
  Azure Databricks, managed identities, and RBAC;
- unit tests and a non-deploying CI workflow.

In production, Azure Data Factory calls OpenWeather directly.

`src/ingestion/openweather_client.py` is used only for local development and API testing. It is not part of the production ingestion path.

## Project Structure

```text
src/                      Local Python client, utilities, and quality rules
config/cities.json        Version-controlled, non-secret city configuration
infrastructure/terraform  Azure infrastructure for MVP 1 and MVP 2
adf/                      ADF artifacts after Git integration
databricks/               RAW, Bronze, Silver, and Gold transformations
sql/                      Reserved for the analytics layer
tests/                    Unit and integration tests
docs/                     Architecture and operational documentation
```

## Local Setup

Python 3.12 is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENWEATHER_API_KEY` in `.env`, then fetch weather data for the cities configured in `config/cities.json`:

```powershell
python -m src.ingestion.openweather_client
```

The command prints the original JSON response returned by OpenWeather for each configured city.

The `.env` file is ignored by Git and must never be committed.

Run the local checks with:

```powershell
python -m pytest -q
```

## Provision the Azure Infrastructure

Prerequisites:

- Azure CLI
- Terraform 1.7 or later
- an Azure subscription
- permissions to create Azure resources and RBAC role assignments

Authenticate and prepare Terraform:

```powershell
az login
az account show

Set-Location infrastructure/terraform
Copy-Item terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and configure:

- your Azure subscription ID;
- a unique suffix containing 3–8 lowercase letters or digits.

Do not store the OpenWeather API key in Terraform variables.

Run:

```powershell
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan -out main.tfplan
terraform apply main.tfplan
```

Terraform creates the Azure foundation, including the `datalake` filesystem,
ADF, the Databricks workspace, and the Databricks Access Connector.

The following logical paths are used by the platform:

```text
datalake/
├── config/
├── raw/
├── bronze/
├── silver/
└── gold/
```

The RAW, Bronze, Silver, and Gold directories are managed by Terraform. The
partition directories below RAW are created by ADF when weather files are written.

## ADF Ingestion Pipeline — MVP 1

After provisioning the infrastructure, create a Key Vault secret named:

```text
openweather-api-key
```

The Azure Data Factory managed identity requires:

- `Key Vault Secrets User` on Azure Key Vault;
- `Storage Blob Data Contributor` on the Storage Account.

The ADF ingestion pipeline follows this workflow:

```text
cities.json
    |
    v
Lookup Cities
    |
    v
Get API Secret
    |
    v
ForEach City
    |
    v
Copy Weather
    |
    v
ADLS Gen2 RAW
```

The detailed flow is:

```text
Lookup cities.json
        |
        v
Read OpenWeather API key from Azure Key Vault
        |
        v
ForEach city
        |
        v
Call OpenWeather API
        |
        v
Write JSON response to ADLS
        |
        v
datalake/raw/weather/...
```

Example RAW storage structure:

```text
datalake/
└── raw/
    └── weather/
        └── year=2026/
            └── month=09/
                └── day=03/
                    └── hour=10/
                        ├── Fes.json
                        ├── Casablanca.json
                        ├── Rabat.json
                        ├── Marrakech.json
                        ├── Tangier.json
                        └── Agadir.json
```

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

locals {
  storage_account_name      = "stweather${var.environment}${var.unique_suffix}"
  key_vault_name            = "kv-weather-${var.environment}-${var.unique_suffix}"
  data_factory_name         = "adf-weather-${var.environment}-${var.unique_suffix}"
  databricks_workspace_name = "dbw-weather-${var.environment}-${var.unique_suffix}"
  databricks_connector_name = "dbc-weather-${var.environment}-${var.unique_suffix}"
}

resource "azurerm_resource_group" "weather" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "weather" {
  name                            = local.storage_account_name
  resource_group_name             = azurerm_resource_group.weather.name
  location                        = azurerm_resource_group.weather.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  is_hns_enabled                  = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = true
}


resource "azurerm_storage_data_lake_gen2_filesystem" "datalake" {
  name               = "datalake"
  storage_account_id = azurerm_storage_account.weather.id
}

resource "azurerm_storage_data_lake_gen2_path" "raw" {
  path               = "raw"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.datalake.name
  storage_account_id = azurerm_storage_account.weather.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "bronze" {
  path               = "bronze"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.datalake.name
  storage_account_id = azurerm_storage_account.weather.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "silver" {
  path               = "silver"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.datalake.name
  storage_account_id = azurerm_storage_account.weather.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "gold" {
  path               = "gold"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.datalake.name
  storage_account_id = azurerm_storage_account.weather.id
  resource           = "directory"
}

resource "azurerm_key_vault" "weather" {
  name                       = local.key_vault_name
  location                   = azurerm_resource_group.weather.location
  resource_group_name        = azurerm_resource_group.weather.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
}

resource "azurerm_data_factory" "weather" {
  name                = local.data_factory_name
  location            = azurerm_resource_group.weather.location
  resource_group_name = azurerm_resource_group.weather.name

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "adf_storage_contributor" {
  scope                = azurerm_storage_account.weather.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_data_factory.weather.identity[0].principal_id
}

resource "azurerm_role_assignment" "adf_key_vault_secrets_user" {
  scope                = azurerm_key_vault.weather.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_data_factory.weather.identity[0].principal_id
}

resource "azurerm_databricks_workspace" "weather" {
  name                = local.databricks_workspace_name
  resource_group_name = azurerm_resource_group.weather.name
  location            = azurerm_resource_group.weather.location
  sku                 = "trial"
}

resource "azurerm_databricks_access_connector" "weather" {
  name                = local.databricks_connector_name
  resource_group_name = azurerm_resource_group.weather.name
  location            = azurerm_resource_group.weather.location

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "databricks_storage_contributor" {
  scope                = azurerm_storage_account.weather.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id = (
    azurerm_databricks_access_connector.weather.identity[0].principal_id
  )
}

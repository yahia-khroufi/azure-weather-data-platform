output "resource_group_name" {
  description = "Resource group containing the platform."
  value       = azurerm_resource_group.weather.name
}

output "storage_account_name" {
  description = "ADLS Gen2 storage account name."
  value       = azurerm_storage_account.weather.name
}

output "data_lake_filesystem_name" {
  description = "ADLS Gen2 filesystem used by the platform."
  value       = azurerm_storage_data_lake_gen2_filesystem.datalake.name
}

output "key_vault_name" {
  description = "Key Vault that will hold the OpenWeather secret."
  value       = azurerm_key_vault.weather.name
}

output "data_factory_name" {
  description = "Azure Data Factory instance name."
  value       = azurerm_data_factory.weather.name
}

output "data_factory_principal_id" {
  description = "Managed identity principal used by ADF for RBAC."
  value       = azurerm_data_factory.weather.identity[0].principal_id
}

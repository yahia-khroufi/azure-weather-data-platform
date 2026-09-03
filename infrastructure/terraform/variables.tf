variable "subscription_id" {
  description = "Azure subscription in which the resources will be created."
  type        = string
  sensitive   = true
}

variable "location" {
  description = "Azure region used by the platform."
  type        = string
  default     = "North Europe"
}

variable "resource_group_name" {
  description = "Name of the platform resource group."
  type        = string
  default     = "rg-weather-dev"
}

variable "environment" {
  description = "Short deployment environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = can(regex("^[a-z0-9]{2,6}$", var.environment))
    error_message = "environment must contain 2 to 6 lowercase letters or digits."
  }
}

variable "unique_suffix" {
  description = "Globally unique lowercase suffix used for Storage, Key Vault, and ADF names."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]{3,8}$", var.unique_suffix))
    error_message = "unique_suffix must contain 3 to 8 lowercase letters or digits."
  }
}

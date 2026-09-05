# Storage and container are bootstrapped separately. See docs/deployment.md.
terraform {
  backend "azurerm" {
    use_azuread_auth = true
  }
}

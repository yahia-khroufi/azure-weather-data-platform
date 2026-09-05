# Deploying DEV with GitHub Actions

## Scope and triggers

`CD DEV` runs the reusable CI (Python tests and Terraform checks), then:

- On a same-repository PR targeting `main`: plans DEV infrastructure with the
  `dev-plan` identity. Fork PRs run checks only.
- On a push to `main`, or a manual run on `main`: creates a fresh plan, applies
  that exact plan, then checks that a second plan reports no changes.
- Deployments and plans share a concurrency group and use remote state locking.
  Running applies are never cancelled by newer commits.

This deploys the resources in `infrastructure/terraform`. ADF pipelines,
triggers, Databricks Jobs, notebook publishing and Unity Catalog configuration
are not yet versioned here. The post-deployment check verifies Terraform
convergence; it does not test ingestion or Gold data. No production deployment
is configured. CI also runs independently on pushes and PRs, so its checks may
appear twice; CD deliberately waits for its own checks of the same revision.

## One-time Azure setup

1. Create a separate storage account and private blob container for Terraform
   state, outside this Terraform configuration. Enable blob versioning and
   soft delete. Make its blob endpoint accessible to the GitHub runner.
2. Create two Microsoft Entra applications/service principals: one for DEV
   deployment and one for PR plans. Add a federated credential to each:
   issuer `https://token.actions.githubusercontent.com`, audience
   `api://AzureADTokenExchange`, and the matching subject:
   - `repo:yahia-khroufi/azure-weather-data-platform:environment:dev`
   - `repo:yahia-khroufi/azure-weather-data-platform:environment:dev-plan`
3. Grant both identities `Storage Blob Data Contributor` on the state
   container (Terraform must read/write state and acquire blob leases).
   Treat access to state as sensitive even for the plan identity.
4. Pre-create the weather resource group and import it into state before the
   first deployment. Give the deployment identity `Contributor` and
   `Role Based Access Control Administrator` on that resource group: the
   configuration creates resources and RBAC assignments. Constrain role
   assignment delegation where possible. Give the plan identity `Reader` on
   the group plus `Storage Account Key Operator Service Role` on the weather
   storage account when it exists: the current provider uses storage keys
   for the filesystem/path resources. This exposes storage data to trusted
   PR code, so restrict who can run plans. Register required Azure resource
   providers using an administrator before CI (including Microsoft.Storage,
   Microsoft.KeyVault, Microsoft.DataFactory, Microsoft.Databricks,
   Microsoft.Compute and Microsoft.Network). The workflow disables automatic
   provider registration so its identities need no subscription-wide write role.

Terraform authenticates directly through GitHub OIDC; no client secret or
`azure/login` step is needed. Do not put the OpenWeather API key in Terraform.

## GitHub setup

Create environments `dev` and `dev-plan` in repository Settings > Environments.
Restrict `dev` deployments to `main`. Restrict `dev-plan` to trusted PR refs;
require a reviewer for that environment if PR authors should not automatically
receive access to Azure state/data. Protect `main` with required reviews and CI.

Set these **environment variables** in both environments:

| Variable | Value |
| --- | --- |
| `AZURE_CLIENT_ID` | Client ID of the identity for this environment |
| `AZURE_TENANT_ID` | Microsoft Entra tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Target subscription ID |
| `AZURE_LOCATION` | Existing resource location, e.g. `North Europe` |
| `TF_RESOURCE_GROUP_NAME` | Existing group, e.g. `rg-weather-dev` |
| `TF_UNIQUE_SUFFIX` | Existing suffix; match deployed names exactly |
| `TF_STATE_STORAGE_ACCOUNT` | Separately bootstrapped state storage account |
| `TF_STATE_CONTAINER` | State container, e.g. `tfstate` |

Both environments must point at the same subscription, resources and state.
The workflow fixes the state key to `weather/dev.tfstate`.

## Existing resources and local state

Do this before enabling the first automatic deployment. Never start from an
empty state against existing resources or change their naming variables.

With Azure CLI login and Terraform 1.11.4 available, back up your existing state
securely. From `infrastructure/terraform`, run the following as one command,
replacing the two placeholders (local authentication uses your Azure CLI):

```text
terraform init -migrate-state -backend-config="storage_account_name=STATE_ACCOUNT" -backend-config="container_name=STATE_CONTAINER" -backend-config="key=weather/dev.tfstate"
```

Use the existing `terraform.tfvars` values and verify `terraform plan` before
merging. If resources were created manually and have no state, import each
existing resource into its matching Terraform address first. For the group:

```text
terraform import azurerm_resource_group.weather /subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP
```

Do not commit state, backend configuration files, plans or secrets. A plan can
contain sensitive data; the workflow keeps it only on the ephemeral runner.

## Operation

Open a PR to see the plan in Actions logs. Merge to `main` to deploy DEV. A
failed check or plan blocks apply. Inspect failed applies before retrying via
Actions > CD DEV > Run workflow on `main`. Terraform state is not rolled back
automatically; resolve the failed resource or revert the code through a PR.

Next, export and version the ADF and Databricks configuration, add their
deployment steps, and add a bounded pipeline run that checks Gold output.

References: [Terraform Azure backend and OIDC](https://developer.hashicorp.com/terraform/language/backend/azurerm),
[AzureRM OIDC authentication](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_oidc).

output "azure_resource_group_name" {
  description = "Name of the provisioned Azure Resource Group."
  value       = azurerm_resource_group.team.name
}

output "azure_resource_group_id" {
  description = "Azure Resource Manager ID of the Resource Group."
  value       = azurerm_resource_group.team.id
}

output "github_repository_url" {
  description = "HTTPS clone URL of the provisioned GitHub repository."
  value       = github_repository.team_infra.html_url
}

output "github_repository_full_name" {
  description = "Full name (org/repo) of the provisioned GitHub repository."
  value       = github_repository.team_infra.full_name
}

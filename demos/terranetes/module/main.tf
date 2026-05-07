terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

# NOTE: No provider "azurerm" block here — Terranetes injects provider.tf.json
# with the azurerm provider config (ARM_* vars from the Provider secret).
# Adding one here causes "Duplicate provider configuration" at init time.

provider "github" {
  owner = var.github_org
  # GITHUB_TOKEN env var is injected by Terranetes from the azure-provider-creds secret.
}

# ── Azure: Resource Group ─────────────────────────────────────────────────────

resource "azurerm_resource_group" "team" {
  name     = "rg-${var.team_name}-${var.environment}"
  location = var.location

  tags = {
    managed-by  = "terranetes"
    team        = var.team_name
    environment = var.environment
    platform    = "true"
  }
}

# ── GitHub: Team infrastructure repository ────────────────────────────────────

resource "github_repository" "team_infra" {
  name        = "${var.team_name}-platform-infra"
  description = "Platform infrastructure repo for team ${var.team_name} — managed by Terranetes"
  visibility  = var.github_repo_visibility

  auto_init = true

  topics = ["platform-engineering", "terranetes", "gitops"]
}

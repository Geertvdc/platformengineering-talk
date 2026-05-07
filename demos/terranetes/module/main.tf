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

provider "azurerm" {
  features {}
  # ARM_* env vars are injected by Terranetes from the azure-provider-creds secret.
}

provider "github" {
  owner = var.github_org
  # GITHUB_TOKEN env var is injected by Terranetes from the github-provider-creds secret.
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

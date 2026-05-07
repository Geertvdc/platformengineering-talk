variable "team_name" {
  description = "Short name for the team (used in resource naming). Lowercase letters and hyphens only."
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,18}[a-z0-9]$", var.team_name))
    error_message = "team_name must be 3–20 lowercase alphanumeric characters or hyphens, starting with a letter."
  }
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

variable "location" {
  description = "Azure region for the resource group."
  type        = string
  default     = "westeurope"
}

variable "github_org" {
  description = "GitHub organisation or username that owns the new repository."
  type        = string
}

variable "github_repo_visibility" {
  description = "GitHub repository visibility."
  type        = string
  default     = "private"

  validation {
    condition     = contains(["public", "private", "internal"], var.github_repo_visibility)
    error_message = "github_repo_visibility must be public, private, or internal."
  }
}

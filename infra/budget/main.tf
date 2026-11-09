terraform {
  required_version = ">= 1.7, < 2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Global budget API; this does not change the application's Stockholm region.
provider "aws" {
  region              = "us-east-1"
  profile             = var.aws_profile
  allowed_account_ids = ["331001679034"]
}

variable "aws_profile" {
  description = "Local AWS profile used only for this budget."
  type        = string
  default     = "andre-ai-lab"
}

variable "alert_email" {
  description = "Budget alert recipient. Supply locally; never commit real addresses."
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$", var.alert_email))
    error_message = "Provide an email address without whitespace."
  }
}

resource "aws_budgets_budget" "monthly" {
  account_id   = "331001679034"
  name         = "andre-ai-lab-monthly"
  budget_type  = "COST"
  limit_amount = "20"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  # No filters: covers all regions and services in this account.
  cost_types {
    include_credit = false
  }

  dynamic "notification" {
    for_each = toset([5, 10, 20])
    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "ABSOLUTE_VALUE"
      notification_type          = "ACTUAL"
      subscriber_email_addresses = [var.alert_email]
    }
  }
}

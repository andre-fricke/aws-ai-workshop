# Mocked plan only: no real provider authentication or AWS API calls.
mock_provider "aws" {}

variables {
  alert_email = "recipient@example.com"
}

run "account_wide_monitoring_contract" {
  command = plan

  assert {
    condition = (
      aws_budgets_budget.monthly.account_id == "331001679034" &&
      aws_budgets_budget.monthly.limit_amount == "20" &&
      aws_budgets_budget.monthly.limit_unit == "USD" &&
      aws_budgets_budget.monthly.time_unit == "MONTHLY" &&
      aws_budgets_budget.monthly.budget_type == "COST" &&
      !aws_budgets_budget.monthly.cost_types[0].include_credit &&
      length(aws_budgets_budget.monthly.cost_filter) == 0
    )
    error_message = "Budget must monitor monthly account-wide USD costs before credits."
  }

  assert {
    condition = (
      length(aws_budgets_budget.monthly.notification) == 3 &&
      toset([for n in aws_budgets_budget.monthly.notification : n.threshold]) == toset([5, 10, 20]) &&
      alltrue([for n in aws_budgets_budget.monthly.notification :
        n.comparison_operator == "GREATER_THAN" &&
        n.threshold_type == "ABSOLUTE_VALUE" &&
        n.notification_type == "ACTUAL" &&
        toset(n.subscriber_email_addresses) == toset([var.alert_email])
      ])
    )
    error_message = "Expected actual-cost email alerts above 5, 10 and 20 USD."
  }
}

run "invalid_recipient_rejected" {
  command = plan
  variables {
    alert_email = "invalid"
  }
  expect_failures = [var.alert_email]
}

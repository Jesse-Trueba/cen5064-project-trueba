# ADR-002: Use Manual Financial Data Entry Instead of External Bank APIs

## Context

The Personal Finance Advisor needs financial information in order to track expenses, budgets, and savings goals. One option would be to connect to external banking services and automatically import transactions. However, this would introduce authentication, security, API availability, and integration complexity that is outside the intended scope of the semester project.

## Decision

Users will manually enter their income, expenses, budgets, and savings information. The application will store and process this information internally and will not connect to live bank accounts or external financial APIs.

## Consequences

This keeps the project focused on software design, business rules, and the four-tier architecture rather than third-party integration. It also avoids handling banking credentials and external API failures.

The tradeoff is that users must enter their financial information manually, and the application will not automatically synchronize with real bank accounts.
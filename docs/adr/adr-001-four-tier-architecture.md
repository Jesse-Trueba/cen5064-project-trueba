# ADR-001: Use a Four-Tier Architecture

## Context

The Personal Finance Advisor needs to support transaction entry, monthly budget comparison, savings goal tracking, and a dashboard while keeping business logic separate from the user interface and data storage. Mixing these responsibilities would make the application harder to test, maintain, and expand during the second half of the semester.

## Decision

The system will use a four-tier architecture:

- Presentation tier: handles user interaction and displays financial information.
- Service tier: coordinates application use cases and connects the presentation layer to the domain and data layers.
- Domain tier: contains core financial objects and business rules, including budget calculations and savings progress.
- Data tier: handles storage and retrieval of transactions, budgets, and savings goals.

Dependencies will flow inward through these tiers. The presentation tier will not directly access the data tier, and business rules will remain in the domain tier instead of the UI.

## Consequences

This structure provides clear separation of responsibilities and makes individual parts of the system easier to test. Domain rules can be tested without requiring the user interface or database.

The tradeoff is that the project requires more classes and interfaces than a simpler single-file application. Even small features may require changes across multiple tiers.
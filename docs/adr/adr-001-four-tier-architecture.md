# ADR-001: Use a Four-Tier Architecture

## Context

The Personal Finance Advisor is intended to help users record financial activity, compare monthly spending against budgets, track savings goals, and view a summary of their finances. These features require user input, application coordination, financial business rules, and persistent storage to work together.

As the project grows during the semester, keeping all of these responsibilities in the same part of the application would make changes harder to manage and test. The architecture therefore needs clear boundaries between user interaction, use-case coordination, financial rules, and data storage.

## Decision

The Personal Finance Advisor will be implemented in Python using a four-tier architecture:

- Presentation tier: handles user interaction and displays financial information.
- Service tier: coordinates application use cases and connects the presentation layer to the domain and data layers.
- Domain tier: contains core financial objects and business rules, including budget calculations and savings progress.
- Data tier: handles storage and retrieval of transactions, budgets, and savings goals.

The specific storage implementation may evolve as the project develops, but storage concerns will remain isolated in the data tier.

Dependencies will flow through these tiers so that the presentation tier does not directly access storage and domain rules remain independent of the user interface.

## Consequences

This structure provides clear separation of responsibilities and makes individual parts of the system easier to test. Domain rules can be tested without requiring the user interface or database.

The tradeoff is that the project requires more classes and interfaces than a simpler single-file application. Even small features may require changes across multiple tiers.
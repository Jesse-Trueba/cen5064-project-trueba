# ADR-003: Use Tkinter for the Graphical User Interface

## Status

Accepted

## Date

November 13, 2026

## Context

The Personal Finance Advisor originally used a command-line interface in `presentation/budget_cli.py`.

During the midterm check-in, the project was required to provide a real graphical user interface so users could interact with the application's budgeting and transaction features without relying on command-line prompts.

The graphical interface needed to support the existing four-tier architecture and allow users to work with budgets and transactions while keeping business rules outside of the Presentation layer.

## Decision

The application will use Python's Tkinter library for its graphical user interface.

The GUI is implemented in `presentation/finance_gui.py` and provides separate tabs for:

- Dashboard
- Transactions
- Budget
- Charts

The Transactions tab allows users to add categorized income and expense transactions and delete one or multiple selected transactions.

The Dashboard displays the selected month's budget, income, expenses, available funds, and budget status.

The Charts tab displays monthly expense totals grouped by category.

The GUI communicates with the Service layer instead of directly implementing business rules or SQL operations.

## Consequences

### Positive

- Tkinter is included with standard Python installations, so the project does not require a separate web framework.
- The application can run locally without a web server.
- Users can interact with the system through graphical controls instead of command-line prompts.
- The GUI preserves the existing four-tier architecture.
- The Presentation layer can be changed in the future without rewriting Domain business rules.

### Negative

- Tkinter provides a simpler visual design than many modern web frameworks.
- The current interface is designed primarily for desktop use.
- More advanced charting or interface styling may require additional libraries in the future.

## Alternatives Considered

### Command-Line Interface

The existing command-line interface was functional but did not satisfy the requirement for a graphical interface.

### Web Application

A web framework could provide a more modern interface, but it would introduce additional dependencies and deployment complexity that were unnecessary for the current project scope.
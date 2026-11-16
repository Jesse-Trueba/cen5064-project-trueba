# ADR-004: Use SQLite for Persistent Data Storage

## Status

Accepted

## Date

November 13, 2026

## Context

The Personal Finance Advisor originally stored application data in a JSON file.

During the midterm check-in, the project was required to replace JSON storage with a real database while keeping persistence behind repository classes so the other architectural tiers would not need to change.

The application needs persistent storage for budgets and transactions across application sessions.

## Decision

The application will use SQLite as its persistent database.

Database initialization and connection handling are located in `data/database.py`.

Persistence is accessed through repository classes, including:

- `BudgetRepository`
- `TransactionRepository`

The repositories translate stored database records into Domain objects before returning them to the Service layer.

Transaction amounts are stored as integer cents in SQLite and converted back to `Decimal` values when Domain objects are reconstructed.

The Presentation and Domain layers do not execute SQL directly.

## Consequences

### Positive

- Data remains available after the application is closed and reopened.
- SQLite provides a real relational database without requiring a separate database server.
- SQL operations remain isolated inside the Data layer.
- Repository abstractions reduce coupling between business logic and the database implementation.
- SQLite supports reliable creation, retrieval, updating, and deletion of application data.

### Negative

- The database currently exists locally on one computer.
- The current implementation does not synchronize financial information between devices.
- Moving to a remote or cloud database in the future would require another repository implementation or changes within the Data layer.

## Alternatives Considered

### JSON Files

JSON was used earlier in the project and was simple to implement, but it provides less structure and database functionality than SQLite.

### Remote Database

A hosted database would support multi-device access, but it would require networking, authentication, deployment, and additional infrastructure beyond the current project scope.
# Personal Finance Advisor
[![CI](https://github.com/Jesse-Trueba/cen5064-project-trueba/actions/workflows/ci.yml/badge.svg)](https://github.com/Jesse-Trueba/cen5064-project-trueba/actions/workflows/ci.yml)

<!-- CI badge: after Session 4, replace ORG/REPO and the workflow filename, then uncomment:
![CI](https://github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg)
-->

**Student:** Jesse Trueba · **Course:** CEN 5064 Software Design, Fall 2026 · **Partner:** @esway001

## Project 

My project will be a personal finance advisor web application designed to help users better understand and manage their money. The system will allow users to record and categorize income and expenses, create monthly budgets and compare their spending against those budgets, set savings goals and track their progress, and view a financial dashboard that summarizes their overall financial activity through balances, spending categories, and other useful information. The goal of the project is to provide a simple and organized way for users to monitor their finances while demonstrating a clear software architecture and well-designed separation between the user interface, business logic, domain objects, and data storage.

## How to Run

### Requirements

- Python 3.12 or newer

### Install dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install pytest ruff
```

### Run the tests

```bash
python -m pytest
```

### Run the budget working slice

```bash
python -m presentation.budget_cli
```

When prompted, enter:

- a budget ID
- a month in YYYY-MM format
- a monthly budget limit
- a total spending amount

The program will save the budget, retrieve it from storage, calculate the remaining amount, determine whether the budget has been exceeded, and display the result.

## Architecture

### Tier breakdown (Session 2 studio)

| Tier | Responsibilities in THIS system |
|------|--------------------------------|
| Presentation | Displays the financial dashboard and forms for entering transactions, budgets, and savings goals. Collects user input and shows results returned by the Service tier. Likely modules: DashboardPage, TransactionForm, BudgetGoalPage. |
| Service | Coordinates the main use cases of the application, such as adding a transaction, creating a budget, and updating a savings goal. It connects the Presentation tier with the Domain and Data tiers. Likely modules: TransactionService, BudgetService, SavingsGoalService. |
| Domain | Contains the main financial entities and business rules. This includes representing transactions, comparing spending against a budget, and calculating progress toward a savings goal. Likely classes: Transaction, Budget, SavingsGoal. |
| Data | Handles saving and retrieving transactions, budgets, and savings goals from the application's single data store. The rest of the system should not need to know how the data is physically stored. Likely modules: TransactionRepository, BudgetRepository, SavingsGoalRepository. |

### C4 — Context & Container (Session 3 studio)

```mermaid
flowchart TB
    user([User]) -->|manages personal finances with| system[Personal Finance Advisor]
```

```mermaid
flowchart TB
    user([User])

    subgraph FinanceAdvisor [Personal Finance Advisor]
        ui[Web User Interface<br/>Presentation]
        app[Finance Advisor Application<br/>Service + Domain]
        db[(Financial Data Store<br/>Data)]
    end

    user -->|enters transactions, budgets, and savings goals| ui
    ui -->|sends requests and displays results| app
    app -->|saves and retrieves financial data| db
```

### UML — Class & Sequence (Session 3 studio)

```mermaid
classDiagram
    class Transaction {
        -id: String
        -description: String
        -amount: double
        -date: Date
        -type: String
        +isExpense() boolean
    }

    class Category {
        -name: String
        -type: String
    }

    class Budget {
        -id: String
        -monthlyLimit: double
        -month: String
        +remainingAmount(totalSpent: double) double
        +isExceeded(totalSpent: double) boolean
    }

    class SavingsGoal {
        -id: String
        -name: String
        -targetAmount: double
        -currentAmount: double
        -targetDate: Date
        +progressPercent() double
        +remainingAmount() double
    }

    Transaction "*" --> "1" Category : categorized as
    Budget "*" --> "1" Category : limits
```

```mermaid
sequenceDiagram
    actor U as User
    participant UI as Dashboard
    participant S as BudgetService
    participant TR as TransactionRepository
    participant BR as BudgetRepository
    participant B as Budget

    U->>UI: view budget status
    UI->>S: getBudgetStatus(category, month)
    S->>TR: findExpenses(category, month)
    TR-->>S: transactions
    S->>BR: findBudget(category, month)
    BR-->>S: budget
    S->>B: compare spending to budget
    B-->>S: remaining amount / exceeded status
    S-->>UI: budget status
    UI-->>U: display spending vs. budget
```

## Architecture Decision Records

Decisions live in [`docs/adr/`](docs/adr/). Start with ADR-001 in Session 4.

| # | Decision | Status |
|---|----------|--------|
| [001](docs/adr/adr-001.md) | [What I am building and why] | [proposed] |

## Weekly log (optional but recommended)

A one-line note per week keeps your commit story readable:

- Week 1 (Aug 24): repo created, three ideas drafted
- Week 2 (Aug 31): ...

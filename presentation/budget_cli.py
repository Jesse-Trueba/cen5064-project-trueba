
from data.budget_repository import BudgetRepository
from service.budget_service import BudgetService


def main() -> None:
    repository = BudgetRepository()
    service = BudgetService(repository)

    print("Personal Finance Advisor")
    print("------------------------")

    budget_id = input("Budget ID: ").strip()
    month = input("Month (YYYY-MM): ").strip()
    monthly_limit = input("Monthly budget limit: $").strip()
    total_spending = input("Total spending: $").strip()

    service.create_budget(
        budget_id=budget_id,
        monthly_limit=monthly_limit,
        month=month,
    )

    status = service.get_budget_status(
        budget_id=budget_id,
        total_spending=total_spending,
    )

    print()
    print("Budget Status")
    print("-------------")
    print(f"Month: {status['month']}")
    print(f"Budget limit: ${status['monthly_limit']:.2f}")
    print(f"Total spending: ${status['total_spending']:.2f}")
    print(f"Remaining: ${status['remaining']:.2f}")

    if status["exceeded"]:
        print("Status: Budget exceeded")
    else:
        print("Status: Within budget")


if __name__ == "__main__":
    main()
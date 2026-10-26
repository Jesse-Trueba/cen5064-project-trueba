import sqlite3
import tkinter as tk
from datetime import UTC, datetime
from decimal import InvalidOperation
from tkinter import messagebox, ttk

from data.budget_repository import BudgetRepository
from data.transaction_repository import TransactionRepository
from domain.transaction import EXPENSE_CATEGORIES, INCOME_CATEGORIES
from service.budget_service import BudgetService
from service.transaction_service import TransactionService


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Advisor")
        self.geometry("900x650")
        self.minsize(800, 550)

        self.budget_repository = BudgetRepository()
        self.transaction_repository = TransactionRepository()

        self.budget_service = BudgetService(
            self.budget_repository,
            self.transaction_repository,
        )

        self.transaction_service = TransactionService(
            self.transaction_repository
        )

        self.current_month = (
            datetime.now(UTC).astimezone().strftime("%Y-%m")
        )

        self.create_widgets()
        self.refresh_transactions()
        self.refresh_dashboard()

    def create_widgets(self):
        title = ttk.Label(
            self,
            text="Personal Finance Advisor",
            font=("Arial", 22, "bold"),
        )
        title.pack(pady=15)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10,
        )

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.budget_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.dashboard_tab,
            text="Dashboard",
        )

        self.notebook.add(
            self.transactions_tab,
            text="Transactions",
        )

        self.notebook.add(
            self.budget_tab,
            text="Budget",
        )

        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_budget_tab()

    def create_dashboard_tab(self):
        frame = ttk.Frame(
            self.dashboard_tab,
            padding=20,
        )
        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Monthly Financial Summary",
            font=("Arial", 16, "bold"),
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10,
        )

        ttk.Label(
            frame,
            text="Month:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8,
        )

        self.dashboard_month_var = tk.StringVar(
            value=self.current_month
        )

        ttk.Entry(
            frame,
            textvariable=self.dashboard_month_var,
            width=20,
        ).grid(
            row=1,
            column=1,
            sticky="w",
        )

        ttk.Button(
            frame,
            text="Refresh Dashboard",
            command=self.refresh_dashboard,
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10,
        )

        self.budget_value = ttk.Label(
            frame,
            text="Budget: --",
            font=("Arial", 14),
        )
        self.budget_value.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
        )

        self.spending_value = ttk.Label(
            frame,
            text="Expenses: --",
            font=("Arial", 14),
        )
        self.spending_value.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
        )

        self.remaining_value = ttk.Label(
            frame,
            text="Remaining: --",
            font=("Arial", 14),
        )
        self.remaining_value.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
        )

        self.status_value = ttk.Label(
            frame,
            text="Status: --",
            font=("Arial", 14, "bold"),
        )
        self.status_value.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8,
        )

    def create_transactions_tab(self):
        form = ttk.Frame(
            self.transactions_tab,
            padding=15,
        )
        form.pack(fill="x")

        self.transaction_date_var = tk.StringVar(
            value=datetime.now(
                UTC
            ).astimezone().date().isoformat()
        )

        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        self.transaction_type_var = tk.StringVar(
            value="expense"
        )

        ttk.Label(
            form,
            text="Date:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        ttk.Entry(
            form,
            textvariable=self.transaction_date_var,
            width=15,
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Description:",
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5,
        )

        ttk.Entry(
            form,
            textvariable=self.description_var,
            width=20,
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Category:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        self.category_box = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=sorted(EXPENSE_CATEGORIES),
            state="readonly",
            width=18,
        )
        self.category_box.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Amount:",
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5,
        )

        ttk.Entry(
            form,
            textvariable=self.amount_var,
            width=20,
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form,
            text="Type:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5,
        )

        type_box = ttk.Combobox(
            form,
            textvariable=self.transaction_type_var,
            values=("expense", "income"),
            state="readonly",
            width=18,
        )
        type_box.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
        )

        # Update the valid categories when the transaction type changes.
        type_box.bind(
            "<<ComboboxSelected>>",
            self.update_category_options,
        )

        ttk.Button(
            form,
            text="Add Transaction",
            command=self.add_transaction,
        ).grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=10,
        )

        table_frame = ttk.Frame(
            self.transactions_tab,
            padding=15,
        )
        table_frame.pack(
            fill="both",
            expand=True,
        )

        columns = (
            "date",
            "description",
            "category",
            "type",
            "amount",
        )

        self.transaction_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )

        self.transaction_table.heading(
            "date",
            text="Date",
        )
        self.transaction_table.heading(
            "description",
            text="Description",
        )
        self.transaction_table.heading(
            "category",
            text="Category",
        )
        self.transaction_table.heading(
            "type",
            text="Type",
        )
        self.transaction_table.heading(
            "amount",
            text="Amount",
        )

        self.transaction_table.column(
            "date",
            width=100,
        )
        self.transaction_table.column(
            "description",
            width=180,
        )
        self.transaction_table.column(
            "category",
            width=140,
        )
        self.transaction_table.column(
            "type",
            width=100,
        )
        self.transaction_table.column(
            "amount",
            width=100,
        )

        self.transaction_table.pack(
            fill="both",
            expand=True,
        )

    def create_budget_tab(self):
        frame = ttk.Frame(
            self.budget_tab,
            padding=20,
        )
        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Monthly Budget",
            font=("Arial", 16, "bold"),
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10,
        )

        self.budget_month_var = tk.StringVar(
            value=self.current_month
        )

        self.budget_limit_var = tk.StringVar()

        ttk.Label(
            frame,
            text="Month (YYYY-MM):",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=10,
        )

        ttk.Entry(
            frame,
            textvariable=self.budget_month_var,
            width=20,
        ).grid(
            row=1,
            column=1,
            pady=10,
        )

        ttk.Label(
            frame,
            text="Monthly Limit:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=10,
        )

        ttk.Entry(
            frame,
            textvariable=self.budget_limit_var,
            width=20,
        ).grid(
            row=2,
            column=1,
            pady=10,
        )

        ttk.Button(
            frame,
            text="Save Budget",
            command=self.save_budget,
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=15,
        )

    def update_category_options(self, _event=None):
        transaction_type = self.transaction_type_var.get()

        if transaction_type == "income":
            categories = sorted(INCOME_CATEGORIES)
        else:
            categories = sorted(EXPENSE_CATEGORIES)

        self.category_box["values"] = categories

        # Clear the previous selection because it may not be
        # valid for the newly selected transaction type.
        self.category_var.set("")

    def save_budget(self):
        try:
            month = self.budget_month_var.get().strip()
            limit = self.budget_limit_var.get().strip()

            self.budget_service.create_or_update_monthly_budget(
                month,
                limit,
            )

            self.dashboard_month_var.set(month)

            messagebox.showinfo(
                "Budget Saved",
                f"Budget for {month} was saved.",
            )

            self.refresh_dashboard()

        except (
            ValueError,
            TypeError,
            InvalidOperation,
            sqlite3.Error,
        ) as exc:
            messagebox.showerror(
                "Error",
                str(exc),
            )

    def add_transaction(self):
        try:
            transaction = (
                self.transaction_service.add_transaction(
                    transaction_date=(
                        self.transaction_date_var.get().strip()
                    ),
                    description=(
                        self.description_var.get().strip()
                    ),
                    category=(
                        self.category_var.get().strip()
                    ),
                    amount=self.amount_var.get().strip(),
                    transaction_type=(
                        self.transaction_type_var.get()
                    ),
                )
            )

            messagebox.showinfo(
                "Transaction Added",
                f"{transaction.description} was saved.",
            )

            self.description_var.set("")
            self.category_var.set("")
            self.amount_var.set("")

            self.refresh_transactions()

            month = transaction.date[:7]
            self.dashboard_month_var.set(month)

            self.refresh_dashboard()

        except (
            ValueError,
            TypeError,
            InvalidOperation,
            sqlite3.Error,
        ) as exc:
            messagebox.showerror(
                "Error",
                str(exc),
            )

    def refresh_transactions(self):
        for row in self.transaction_table.get_children():
            self.transaction_table.delete(row)

        transactions = (
            self.transaction_service.get_all_transactions()
        )

        for transaction in transactions:
            if transaction.transaction_type == "expense":
                sign = "-"
            else:
                sign = "+"

            self.transaction_table.insert(
                "",
                "end",
                values=(
                    transaction.date,
                    transaction.description,
                    transaction.category,
                    transaction.transaction_type.title(),
                    f"{sign}${transaction.amount:.2f}",
                ),
            )

    def refresh_dashboard(self):
        month = self.dashboard_month_var.get().strip()

        try:
            status = (
                self.budget_service.get_budget_status_for_month(
                    month
                )
            )

            self.budget_value.config(
                text=(
                    f"Budget: "
                    f"${status['monthly_limit']:.2f}"
                )
            )

            self.spending_value.config(
                text=(
                    f"Expenses: "
                    f"${status['total_spending']:.2f}"
                )
            )

            self.remaining_value.config(
                text=(
                    f"Remaining: "
                    f"${status['remaining']:.2f}"
                )
            )

            if status["exceeded"]:
                status_text = "OVER BUDGET"
            else:
                status_text = "WITHIN BUDGET"

            self.status_value.config(
                text=f"Status: {status_text}"
            )

        except ValueError:
            self.budget_value.config(
                text="Budget: No budget saved"
            )

            self.spending_value.config(
                text="Expenses: --"
            )

            self.remaining_value.config(
                text="Remaining: --"
            )

            self.status_value.config(
                text="Status: --"
            )


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
import sqlite3
import tkinter as tk
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk

from config.app_config import AppConfig
from data.budget_repository import BudgetRepository
from data.transaction_repository import TransactionRepository
from domain.transaction import EXPENSE_CATEGORIES, INCOME_CATEGORIES
from service.budget_service import BudgetService
from service.transaction_service import TransactionService


class FinanceApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Personal Finance Advisor")
        self.root.geometry("900x650")

        self.config = AppConfig()

        self.budget_repository = BudgetRepository(
            self.config.database_path
        )
        self.transaction_repository = TransactionRepository(
            self.config.database_path
        )

        self.budget_service = BudgetService(
            self.budget_repository,
            self.transaction_repository,
        )
        self.transaction_service = TransactionService(
            self.transaction_repository
        )

        now = datetime.now(UTC).astimezone()
        self.current_month = now.strftime("%Y-%m")
        self.current_date = now.strftime("%Y-%m-%d")

        self.create_widgets()
        self.refresh_transactions()
        self.refresh_dashboard()
        self.refresh_chart()

    def create_widgets(self) -> None:
        title = ttk.Label(
            self.root,
            text="Personal Finance Advisor",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.budget_tab = ttk.Frame(self.notebook)
        self.chart_tab = ttk.Frame(self.notebook)

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
        self.notebook.add(
            self.chart_tab,
            text="Charts",
        )

        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_budget_tab()
        self.create_chart_tab()

    def create_dashboard_tab(self) -> None:
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
            text="Monthly Dashboard",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        month_frame = ttk.Frame(frame)
        month_frame.pack(pady=10)

        ttk.Label(
            month_frame,
            text="Month:",
        ).pack(
            side="left",
            padx=5,
        )

        self.dashboard_month_var = tk.StringVar(
            value=self.current_month
        )

        ttk.Entry(
            month_frame,
            textvariable=self.dashboard_month_var,
            width=12,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            month_frame,
            text="Refresh Dashboard",
            command=self.refresh_dashboard,
        ).pack(
            side="left",
            padx=5,
        )

        self.budget_label = ttk.Label(
            frame,
            text="Budget: --",
            font=("Arial", 14),
        )
        self.budget_label.pack(pady=8)

        self.income_label = ttk.Label(
            frame,
            text="Income: --",
            font=("Arial", 14),
        )
        self.income_label.pack(pady=8)

        self.expenses_label = ttk.Label(
            frame,
            text="Expenses: --",
            font=("Arial", 14),
        )
        self.expenses_label.pack(pady=8)

        self.available_funds_label = ttk.Label(
            frame,
            text="Available Funds: --",
            font=("Arial", 14),
        )
        self.available_funds_label.pack(pady=8)

        self.status_label = ttk.Label(
            frame,
            text="Status: --",
            font=("Arial", 14, "bold"),
        )
        self.status_label.pack(pady=8)

    def create_transactions_tab(self) -> None:
        frame = ttk.Frame(
            self.transactions_tab,
            padding=20,
        )
        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Add Transaction",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        form_frame = ttk.Frame(frame)
        form_frame.pack(
            fill="x",
            pady=10,
        )

        ttk.Label(
            form_frame,
            text="Date:",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.transaction_date_var = tk.StringVar(
            value=self.current_date
        )

        ttk.Entry(
            form_frame,
            textvariable=self.transaction_date_var,
            width=15,
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form_frame,
            text="Description:",
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.description_var = tk.StringVar()

        ttk.Entry(
            form_frame,
            textvariable=self.description_var,
            width=20,
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form_frame,
            text="Type:",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.transaction_type_var = tk.StringVar(
            value="expense"
        )

        self.type_box = ttk.Combobox(
            form_frame,
            textvariable=self.transaction_type_var,
            values=["expense", "income"],
            state="readonly",
            width=12,
        )
        self.type_box.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        self.type_box.bind(
            "<<ComboboxSelected>>",
            self.update_category_options,
        )

        ttk.Label(
            form_frame,
            text="Category:",
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.category_var = tk.StringVar()

        self.category_box = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            state="readonly",
            width=18,
        )
        self.category_box.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form_frame,
            text="Amount:",
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.amount_var = tk.StringVar()

        ttk.Entry(
            form_frame,
            textvariable=self.amount_var,
            width=15,
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Button(
            form_frame,
            text="Add Transaction",
            command=self.add_transaction,
        ).grid(
            row=2,
            column=2,
            columnspan=2,
            padx=5,
            pady=10,
        )

        self.update_category_options()

        ttk.Separator(
            frame,
            orient="horizontal",
        ).pack(
            fill="x",
            pady=10,
        )

        ttk.Label(
            frame,
            text="Saved Transactions",
            font=("Arial", 14, "bold"),
        ).pack(pady=5)

        columns = (
            "date",
            "description",
            "category",
            "type",
            "amount",
        )

        self.transaction_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="extended",
            height=8,
        )

        self.transaction_tree.heading(
            "date",
            text="Date",
        )
        self.transaction_tree.heading(
            "description",
            text="Description",
        )
        self.transaction_tree.heading(
            "category",
            text="Category",
        )
        self.transaction_tree.heading(
            "type",
            text="Type",
        )
        self.transaction_tree.heading(
            "amount",
            text="Amount",
        )

        self.transaction_tree.column(
            "date",
            width=100,
        )
        self.transaction_tree.column(
            "description",
            width=200,
        )
        self.transaction_tree.column(
            "category",
            width=140,
        )
        self.transaction_tree.column(
            "type",
            width=100,
        )
        self.transaction_tree.column(
            "amount",
            width=100,
        )

        self.transaction_tree.pack(
            fill="both",
            expand=True,
            pady=10,
        )

        ttk.Button(
            frame,
            text="Delete Selected Transactions",
            command=self.delete_selected_transactions,
        ).pack(pady=10)

    def create_budget_tab(self) -> None:
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
        ).pack(pady=10)

        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=20)

        ttk.Label(
            form_frame,
            text="Month:",
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.budget_month_var = tk.StringVar(
            value=self.current_month
        )

        ttk.Entry(
            form_frame,
            textvariable=self.budget_month_var,
            width=15,
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Label(
            form_frame,
            text="Monthly Limit:",
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="e",
        )

        self.budget_limit_var = tk.StringVar()

        ttk.Entry(
            form_frame,
            textvariable=self.budget_limit_var,
            width=15,
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        ttk.Button(
            form_frame,
            text="Save Budget",
            command=self.save_budget,
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10,
        )

    def create_chart_tab(self) -> None:
        frame = ttk.Frame(
            self.chart_tab,
            padding=20,
        )
        frame.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            frame,
            text="Expense Chart",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        controls = ttk.Frame(frame)
        controls.pack(pady=5)

        ttk.Label(
            controls,
            text="Month:",
        ).pack(
            side="left",
            padx=5,
        )

        self.chart_month_var = tk.StringVar(
            value=self.current_month
        )

        ttk.Entry(
            controls,
            textvariable=self.chart_month_var,
            width=12,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Button(
            controls,
            text="Refresh Chart",
            command=self.refresh_chart,
        ).pack(
            side="left",
            padx=5,
        )

        ttk.Label(
            frame,
            text="Expenses by Category",
            font=("Arial", 12),
        ).pack(pady=5)

        self.chart_canvas = tk.Canvas(
            frame,
            width=800,
            height=400,
            highlightthickness=1,
        )
        self.chart_canvas.pack(
            fill="both",
            expand=True,
            pady=10,
        )

    def update_category_options(self, _event=None) -> None:
        transaction_type = self.transaction_type_var.get()

        if transaction_type == "income":
            categories = sorted(INCOME_CATEGORIES)
        else:
            categories = sorted(EXPENSE_CATEGORIES)

        self.category_box["values"] = categories

        if categories:
            self.category_var.set(categories[0])

    def save_budget(self) -> None:
        try:
            month = self.budget_month_var.get().strip()
            monthly_limit = self.budget_limit_var.get().strip()

            self.budget_service.create_or_update_monthly_budget(
                month=month,
                monthly_limit=monthly_limit,
            )

            self.dashboard_month_var.set(month)

            self.refresh_dashboard()

            messagebox.showinfo(
                "Budget Saved",
                f"Budget for {month} was saved.",
            )

        except (
            ValueError,
            TypeError,
            InvalidOperation,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Budget Error",
                str(error),
            )

    def add_transaction(self) -> None:
        try:
            transaction = (
                self.transaction_service.add_transaction(
                    transaction_date=(
                        self.transaction_date_var.get().strip()
                    ),
                    description=(
                        self.description_var.get().strip()
                    ),
                    category=self.category_var.get().strip(),
                    amount=self.amount_var.get().strip(),
                    transaction_type=(
                        self.transaction_type_var.get()
                    ),
                )
            )

            self.description_var.set("")
            self.amount_var.set("")

            self.refresh_transactions()
            self.refresh_dashboard()
            self.refresh_chart()

            messagebox.showinfo(
                "Transaction Added",
                f"{transaction.description} was saved.",
            )

        except (
            ValueError,
            TypeError,
            InvalidOperation,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Transaction Error",
                str(error),
            )

    def delete_selected_transactions(self) -> None:
        selected_items = self.transaction_tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "No Selection",
                (
                    "Please select at least one "
                    "transaction to delete."
                ),
            )
            return

        transaction_ids = list(selected_items)

        confirmed = messagebox.askyesno(
            "Delete Transactions",
            (
                "Are you sure you want to delete "
                f"{len(transaction_ids)} "
                "selected transaction(s)?"
            ),
        )

        if not confirmed:
            return

        try:
            self.transaction_service.delete_transactions(
                transaction_ids
            )

            self.refresh_transactions()
            self.refresh_dashboard()
            self.refresh_chart()

            messagebox.showinfo(
                "Transactions Deleted",
                "The selected transactions were deleted.",
            )

        except (
            ValueError,
            TypeError,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Delete Error",
                str(error),
            )

    def refresh_transactions(self) -> None:
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        transactions = (
            self.transaction_service.get_all_transactions()
        )

        for transaction in transactions:
            if transaction.transaction_type == "expense":
                sign = "-"
            else:
                sign = "+"

            self.transaction_tree.insert(
                "",
                "end",
                iid=transaction.id,
                values=(
                    transaction.date,
                    transaction.description,
                    transaction.category,
                    transaction.transaction_type.title(),
                    f"{sign}${transaction.amount:.2f}",
                ),
            )

    def refresh_dashboard(self) -> None:
        month = self.dashboard_month_var.get().strip()

        try:
            income = (
                self.transaction_service
                .get_monthly_income_total(month)
            )

            expenses = (
                self.transaction_service
                .get_monthly_expense_total(month)
            )

        except (
            ValueError,
            TypeError,
            InvalidOperation,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Dashboard Error",
                str(error),
            )
            return

        self.income_label.config(
            text=f"Income: ${income:.2f}"
        )

        self.expenses_label.config(
            text=f"Expenses: ${expenses:.2f}"
        )

        try:
            status = (
                self.budget_service
                .get_budget_status_for_month(month)
            )

        except ValueError:
            available_funds = income - expenses

            self.budget_label.config(
                text="Budget: No budget saved"
            )

            self.available_funds_label.config(
                text=(
                    "Available Funds: "
                    f"${available_funds:.2f}"
                )
            )

            self.status_label.config(
                text="Status: --"
            )

            return

        budget = status["monthly_limit"]

        available_funds = (
            budget
            + income
            - expenses
        )

        self.budget_label.config(
            text=f"Budget: ${budget:.2f}"
        )

        self.available_funds_label.config(
            text=(
                "Available Funds: "
                f"${available_funds:.2f}"
            )
        )

        if status["exceeded"]:
            status_text = "OVER BUDGET"
        else:
            status_text = "WITHIN BUDGET"

        self.status_label.config(
            text=f"Status: {status_text}"
        )

    def refresh_chart(self) -> None:
        month = self.chart_month_var.get().strip()

        try:
            transactions = (
                self.transaction_service
                .get_transactions_for_month(month)
            )

        except (
            ValueError,
            TypeError,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Chart Error",
                str(error),
            )
            return

        category_totals = {}

        for transaction in transactions:
            if transaction.transaction_type != "expense":
                continue

            if transaction.category not in category_totals:
                category_totals[transaction.category] = Decimal(0)

            category_totals[
                transaction.category
            ] += transaction.amount

        self.chart_canvas.delete("all")
        self.chart_canvas.update_idletasks()

        width = max(
            self.chart_canvas.winfo_width(),
            800,
        )
        height = max(
            self.chart_canvas.winfo_height(),
            400,
        )

        self.chart_canvas.create_text(
            width / 2,
            25,
            text=f"{month} Expenses by Category",
            font=("Arial", 14, "bold"),
        )

        if not category_totals:
            self.chart_canvas.create_text(
                width / 2,
                height / 2,
                text=(
                    "No expense transactions "
                    "for this month."
                ),
                font=("Arial", 13),
            )
            return

        sorted_categories = sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        max_total = max(
            category_totals.values()
        )

        left_margin = 170
        right_margin = 100
        top_margin = 60
        bottom_margin = 30

        chart_height = (
            height
            - top_margin
            - bottom_margin
        )

        row_height = (
            chart_height
            / len(sorted_categories)
        )

        max_bar_width = (
            width
            - left_margin
            - right_margin
        )

        for index, (
            category,
            total,
        ) in enumerate(sorted_categories):
            y_center = (
                top_margin
                + row_height * index
                + row_height / 2
            )

            bar_height = min(
                30,
                row_height * 0.6,
            )

            y1 = y_center - bar_height / 2
            y2 = y_center + bar_height / 2

            if max_total > 0:
                bar_width = (
                    float(total / max_total)
                    * max_bar_width
                )
            else:
                bar_width = 0

            self.chart_canvas.create_text(
                left_margin - 10,
                y_center,
                text=category,
                anchor="e",
                font=("Arial", 11),
            )

            self.chart_canvas.create_rectangle(
                left_margin,
                y1,
                left_margin + bar_width,
                y2,
                fill="#4A90E2",
                outline="",
            )

            self.chart_canvas.create_text(
                left_margin + bar_width + 10,
                y_center,
                text=f"${total:.2f}",
                anchor="w",
                font=("Arial", 11),
            )


def main() -> None:
    root = tk.Tk()
    FinanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
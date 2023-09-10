import matplotlib.pyplot as plt
import sqlite3
from collections import defaultdict
from datetime import datetime
import budget_planner
import expense_tracker

def main(username):
    db_file = f'{username}_expense_tracker.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Initialize the SQLite database in case user forgot to set it
    expense_tracker.create_user_expenses_table(cursor, username)

    cursor.execute(f"SELECT * FROM expenses_{username}")
    expenses_data = cursor.fetchall()
    conn.close()

    # Initialize expenses and budget
    total_expenses = 0.0
    total_budget = 0.0

    # Create a dictionary to accumulate expenses by month
    expense_totals_by_month = defaultdict(float)

    # Process expenses data
    for expense in expenses_data:
        date_str = expense[3]
        amount = expense[2]

        # Convert amount to float (if it's not already)
        if isinstance(amount, str):
            try:
                amount = float(amount)
            except ValueError:
                amount = 0.0

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Group expenses by month
        month_key = date.strftime('%Y-%m')
        expense_totals_by_month[month_key] += amount

    db_file = f'{username}_budget_tracker.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Initialize the SQLite database in case user forgot to set it
    budget_planner.create_budget_table(cursor, username)

    cursor.execute(f"SELECT * FROM {username}_budget")
    budget_data = cursor.fetchall()
    conn.close()

    # Process budget data
    for budget in budget_data:
        total_budget += budget[1]

    # Display the total expenses and total budget
    months = list(expense_totals_by_month.keys())
    expense_amounts = list(expense_totals_by_month.values())

    # Calculate the maximum value between total expenses and total budget
    max_total = max(total_expenses, total_budget)

    # Set a custom title for the graph
    plt.figure(num="Monthly Expense and Budget Comparison")

    # Plot the graph
    plt.plot(months, expense_amounts, marker='o', label='Expenses', linestyle='-', color='red')
    plt.axhline(y=total_budget, color='green', linestyle='--', label='Budget')
    plt.ylim(0, max_total)  # Set y-axis limits

    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Expense and Budget Comparison Over Time")
    plt.legend()
    plt.grid(True)

    # Display the line graph
    plt.tight_layout()
    plt.xticks(rotation=45, ha="right")
    plt.show()
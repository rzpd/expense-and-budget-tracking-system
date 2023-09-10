import sqlite3

def create_budget_table(cursor, username):
    table_name = f'{username}_budget'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_amount REAL
        )
    ''')
    cursor.connection.commit()

def create_savings_goals_table(cursor, username):
    table_name = f'{username}_savings_goals'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT,
            goal_amount REAL
        )
    ''')
    cursor.connection.commit()

def create_user_budget_database(username):
    db_name = f'{username}_budget_tracker.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create budget and savings goals tables
    create_budget_table(cursor, username)
    create_savings_goals_table(cursor, username)
    
    conn.close()

def add_monthly_budget(cursor, username):
    table_name = f'{username}_budget'
    print("\nBudget Planning - Create Monthly Budget")
    while True:
        try:
            budget_amount = float(input("Enter the budget amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
    
    cursor.execute(f"INSERT INTO {table_name} (budget_amount) VALUES (?)", (budget_amount,))
    cursor.connection.commit()
    print("Budget category added successfully!")

def view_monthly_budget(cursor, username):
    table_name = f'{username}_budget'
    print("\nBudget Planning - View Monthly Budget")
    cursor.execute(f"SELECT * FROM {table_name}")
    budgets = cursor.fetchall()

    if not budgets:
        print("No monthly budget defined yet.")
    else:
        print("\nBudget Amount")
        for budget in budgets:
            print(f"{budget[1]}")

def update_monthly_budget(cursor, username):
    table_name = f'{username}_budget'
    print("\nBudget Planning - Update Budget")

    while True:
        try:
            new_budget_amount = float(input("Enter the new budget amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    cursor.execute(f"UPDATE {table_name} SET budget_amount = ?", (new_budget_amount,))
    cursor.connection.commit()
    print("Budget updated successfully!")

def create_savings_goal(cursor, username):
    table_name = f'{username}_savings_goals'
    print("\nBudget Planning - Create Savings Goal")
    
    # Check if there is an existing goal
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    goal_count = cursor.fetchone()[0]
    
    if goal_count > 0:
        confirmation = input("Warning: Creating a new goal will erase your last goal. Continue? (y/n): ")
        
        if confirmation.lower() != 'y':
            print("Goal creation canceled.")
            return
    
    goal_name = input("Enter a savings goal name: ")
    
    while True:
        try:
            goal_amount = float(input("Enter the goal amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
    
    # Delete the existing goal if it exists
    if goal_count > 0:
        cursor.execute(f"DELETE FROM {table_name}")
    
    cursor.execute(f"INSERT INTO {table_name} (goal_name, goal_amount) VALUES (?, ?)", (goal_name, goal_amount))
    cursor.connection.commit()
    print("Savings goal added successfully!")

def view_savings_goals(cursor, username):
    table_name = f'{username}_savings_goals'
    print("\nBudget Planning - View Savings Goals")
    cursor.execute(f"SELECT * FROM {table_name}")
    savings_goals = cursor.fetchall()

    if not savings_goals:
        print("No savings goals defined yet.")
    else:
        print("\nGoal Name | Goal Amount")
        for goal in savings_goals:
            print(f"{goal[1]} | {goal[2]}")

def update_savings_goal(cursor, username):
    table_name = f'{username}_savings_goals'
    print("\nBudget Planning - Update Savings Goal")

    while True:
        try:
            new_goal_amount = float(input("Enter the new goal amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    cursor.execute(f"UPDATE {table_name} SET goal_amount = ?", (new_goal_amount,))
    cursor.connection.commit()
    print("Savings goal updated successfully!")

# Main program loop
def main(username):
    db_name = f'{username}_budget_tracker.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    create_budget_table(cursor, username)
    create_savings_goals_table(cursor, username)
    
    while True:
        print("\nOptions:")
        print("1. Create Monthly Budget")
        print("2. View Monthly Budget")
        print("3. Update Monthly Budget")
        print("4. Create Savings Goal")
        print("5. View Savings Goals")
        print("6. Update Savings Goals")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_monthly_budget(cursor, username)
        elif choice == '2':
            view_monthly_budget(cursor, username)
        elif choice == '3':
            update_monthly_budget(cursor, username)
        elif choice == '4':
            create_savings_goal(cursor, username)
        elif choice == '5':
            view_savings_goals(cursor, username)
        elif choice == '6':
            update_savings_goal(cursor, username)
        elif choice == '7':
            conn.close()  # Close the database connection
            break
        else:
            print("Invalid choice. Please try again.")
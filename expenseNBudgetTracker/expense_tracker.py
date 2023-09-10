import sqlite3

def create_user_expenses_table(cursor, username):
    table_name = f'expenses_{username}'  # Create a table name based on the username
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date DATE,
            archived INTEGER DEFAULT 0  -- Default value is 0 (not archived)
        )
    ''')

def create_user_archived_expenses_table(cursor, username):
    table_name = f'archived_expenses_{username}'  # Create an archived expenses table based on the username
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date DATE
        )
    ''')
    cursor.connection.commit()

    # Check if the 'archived' column exists, and if not, add it
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'archived' not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN archived INTEGER DEFAULT 0")

    cursor.connection.commit()

# Function to record a new expense
def record_expense(cursor, username):
    # Create the user-specific 'expenses' table if it doesn't exist
    create_user_expenses_table(cursor, username)

    print("Expense Tracking - Record Expense")
    description = input("Enter a description: ")

    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    date = input("Enter the date (YYYY-MM-DD): ")

    # Insert expense data into the user-specific table
    table_name = f'expenses_{username}'
    cursor.execute(f"INSERT INTO {table_name} (description, amount, date) VALUES (?, ?, ?)",
                   (description, amount, date))
    cursor.connection.commit()
    print("Expense recorded successfully!")

# Function to view expenses
def view_expenses(cursor, username):
    print("\nExpense Tracking - View Expenses")

    # Check if the user-specific 'expenses' table exists
    table_name = f'expenses_{username}'
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    table_exists = cursor.fetchone()

    if not table_exists:
        print("No expenses recorded yet.")
    else:
        # Fetch expenses from the user-specific table
        cursor.execute(f"SELECT * FROM {table_name}")
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses recorded yet.")
        else:
            print("\nExpense ID | Description | Amount | Date")
            for expense in expenses:
                print(f"{expense[0]} | {expense[1]} | {expense[2]} | {expense[3]}")

# Function to archive an expense
def archive_expense(cursor, username):
    # Create the user-specific 'archived_expenses' table if it doesn't exist
    create_user_archived_expenses_table(cursor, username)

    print("\nExpense Tracking - Archive Expense")
    while True:
        try:
            expense_id = int(input("Enter the Expense ID to archive: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid Expense ID.")

    # Check if the expense ID exists in the user-specific table
    expenses_table_name = f'expenses_{username}'
    cursor.execute(f"SELECT * FROM {expenses_table_name} WHERE id=?", (expense_id,))
    expense_data = cursor.fetchone()

    if not expense_data:
        print("Expense not found.")
    else:
        # Copy the expense to the user-specific archived expenses table
        archived_table_name = f'archived_expenses_{username}'
        cursor.execute(f"INSERT INTO {archived_table_name} (description, amount, date) VALUES (?, ?, ?)",
                       (expense_data[1], expense_data[2], expense_data[3]))
        cursor.connection.commit()

        # Delete the expense from the user-specific expenses table
        cursor.execute(f"DELETE FROM {expenses_table_name} WHERE id=?", (expense_id,))
        cursor.connection.commit()

        print("Expense archived successfully!")

# Function to view archived expenses
def view_archived_expenses(cursor, username):
    # Create the user-specific 'archived_expenses' table if it doesn't exist
    create_user_archived_expenses_table(cursor, username)

    print("Expense Tracking - View Archived Expenses")
    archived_table_name = f'archived_expenses_{username}'
    cursor.execute(f"SELECT * FROM {archived_table_name}")
    archived_expenses = cursor.fetchall()

    if not archived_expenses:
        print("No archived expenses.")
    else:
        print("\nExpense ID | Description | Amount | Date")
        for expense in archived_expenses:
            print(f"{expense[0]} | {expense[1]} | {expense[2]} | {expense[3]}")

def main(username):
    # Initialize the SQLite database
    conn = sqlite3.connect(f'{username}_expense_tracker.db')
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Record Expense")
        print("2. View Expenses")
        print("3. Archive Expenses")
        print("4. View archived expenses")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            record_expense(cursor, username)
        elif choice == '2':
            view_expenses(cursor, username)
        elif choice == '3':
            archive_expense(cursor, username)
        elif choice == '4':
            view_archived_expenses(cursor, username)
        elif choice == '5':
            conn.close()
            break
import sqlite3
import bcrypt
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import expense_tracker
import budget_planner
import budget_tracker_gui

# Initialize the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a users table to store user data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
''')
conn.commit()

def validate_username(cursor):
    while True:
        username = input("Enter a username (letters and numbers only, no spaces): ")
        if not username.isalnum():
            print("Username should contain only letters and numbers.")
        else:
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                print("Username already exists. Please choose another.")
            else:
                return username
            
def validate_email():
    while True:
        email = input("Enter your email address: ")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("Invalid email address.")
        else:
            return email
        
def send_verification_email(email, verification_code):
    # Your Gmail email and password
    email_sender = 'youremail@gmail.com'
    email_app_password = 'yourEmailAppPassword' # I recommend using email app password as google doesn't allow normal password to log in from a suspicious file like python script

    # Create the email message
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the Gmail SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_app_password)

        # Send the email
        server.sendmail(email_sender, email, msg.as_string())
        server.quit()
        print("Verification code sent successfully.")
    except Exception as e:
        print(f"Failed to send verification email: {e}")

def validate_verification_code(verification_code):
    while True:
        user_input_verification_code = input("Enter the verification code from your email: ")
        if user_input_verification_code == verification_code:
            print("Email verified!")
            return True
        else:
            print("Invalid verification code. Please try again.")

def validate_password():
    while True:
        password = input("Enter a password: ")
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            print("Password does not meet the required criteria.")
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed_password

# Function to register a new user
def register(cursor):
    print("\nUser Registration")
    username = validate_username(cursor)
    email = validate_email()

    verification_code = str(random.randint(1000, 9999))
    send_verification_email(email, verification_code)
    if not validate_verification_code(verification_code):
        print("Email verification failed. Registration aborted.")
        return

    hashed_password = validate_password()
    
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
    conn.commit()
    print("Registration successful!")

# Function to log in
def login(cursor):
    print("\nUser Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Retrieve user data from the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if not user_data:
        print("Invalid username or password.")
        return

    # Check if the password is correct
    if bcrypt.checkpw(password.encode('utf-8'), user_data[2]):
        handle_successful_login(username)
    else:
        print("Invalid username or password.")

def handle_successful_login(username):
    print("Login successful!")
    while True:
        print("\nOptions:")
        print("1. Expense Tracker")
        print("2. Budget Planner")
        print("3. GUI")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            # Call the function to start the expense tracker from the expense_tracker.py file
            expense_tracker.main(username)
        elif choice == '2':
            # Call the function to start the budget planner from the budget_planner.py file
            budget_planner.main(username)
        elif choice == '3':
            # Call the function to shows user the graphical representation of monthly spending from the budget_tracker_gui.py file
            budget_tracker_gui.main(username)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Main program loop
while True:
    print("\nOptions:")
    print("1. Register")
    print("2. Login")
    print("3. Quit")

    choice = input("Choose an option: ")

    if choice == '1':
        register(cursor)
    elif choice == '2':
        login(cursor)
    elif choice == '3':
        conn.close()  # Close the database connection
        break
    else:
        print("Invalid choice. Please try again.")

"""
SpendWise - Student Expense Manager
Python Essentials Course Project

A simple CLI tool to track daily expenses and monthly budgets.
Built using only the Python standard library + SQLite.
"""

from datetime import date, datetime

from src.database import initialize_database
from src.user import create_user, get_user, get_user_by_email
from src.expense import (
    add_expense,
    get_expenses,
    get_expense,
    update_expense,
    delete_expense,
    search_expenses
)
from src.budget import (
    set_budget,
    get_budget_status
)
from src.reports import (
    get_total_expenses,
    get_category_summary,
    get_highest_expense,
    get_monthly_summary
)
from src.validation import (
    validate_name,
    validate_email,
    validate_amount
)

from src.utils import (
    clear_screen,
    print_logo,
    print_section,
    print_success,
    print_error,
    print_warning,
    print_info,
    format_currency,
    progress_bar,
    pause,
    choose_category
)


# GENERAL HELPERS

def get_current_month():
    """Return the current month in YYYY-MM format."""
    return date.today().strftime("%Y-%m")


def get_today():
    """Return today's date in YYYY-MM-DD format."""
    return date.today().strftime("%Y-%m-%d")


def validate_date(date_text):
    """Validate a date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_valid_amount(prompt):
    """Keep asking until a valid positive amount is entered."""
    while True:
        value = input(prompt).strip()

        if validate_amount(value):
            return float(value)

        print_error("Please enter a valid positive amount.")


def get_valid_date():
    """Ask the user for a valid date."""
    while True:
        value = input(
            "  Date [YYYY-MM-DD] "
            f"(Enter = {get_today()}): "
        ).strip()

        if not value:
            return get_today()

        if validate_date(value):
            return value

        print_error("Invalid date. Use YYYY-MM-DD.")


# PROFILE SYSTEM

def create_profile():
    """Create a new student profile."""

    clear_screen()
    print_logo()
    print_section("CREATE NEW PROFILE")

    print()

    while True:
        name = input("  Enter your name: ").strip()

        if validate_name(name):
            break

        print_error("Name should contain letters and spaces only.")

    while True:
        email = input("  Enter your email: ").strip()

        if not validate_email(email):
            print_error("Please enter a valid email address.")
            continue

        if get_user_by_email(email):
            print_warning("An account with this email already exists.")
            print_info("Please use the login option instead.")
            pause()
            return None

        break

    user_id = create_user(name, email)

    if user_id is None:
        print_error("Could not create the profile.")
        pause()
        return None

    print()
    print_success("Profile created successfully!")
    print_info(f"Welcome to SpendWise, {name}.")

    pause()

    return get_user(user_id)


def login():
    """Login using an existing email."""

    clear_screen()
    print_logo()
    print_section("LOGIN")

    print()

    email = input("  Enter your registered email: ").strip()

    user = get_user_by_email(email)

    if user is None:
        print()
        print_error("No account found with this email.")
        pause()
        return None

    print()
    print_success(f"Welcome back, {user['name']}!")

    pause()

    return user


def profile_menu(user):
    """Display and manage the user profile."""

    while True:
        clear_screen()
        print_logo()
        print_section("PROFILE")

        print()
        print(f"  Name  : {user['name']}")
        print(f"  Email : {user['email']}")
        print(f"  User ID: {user['id']}")

        print()
        print("  [1] Update Profile")
        print("  [0] Back")

        choice = input("\n  Choose an option: ").strip()

        if choice == "1":
            update_profile(user)
        elif choice == "0":
            return
        else:
            print_error("Invalid option.")
            pause()


def update_profile(user):
    """Update profile information."""

    clear_screen()
    print_logo()
    print_section("UPDATE PROFILE")

    print()

    name = input(
        f"  Name [{user['name']}]: "
    ).strip()

    if not name:
        name = user["name"]

    if not validate_name(name):
        print_error("Invalid name.")
        pause()
        return

    email = input(
        f"  Email [{user['email']}]: "
    ).strip()

    if not email:
        email = user["email"]

    if not validate_email(email):
        print_error("Invalid email.")
        pause()
        return

    existing = get_user_by_email(email)

    if existing and existing["id"] != user["id"]:
        print_error("That email is already being used.")
        pause()
        return

    from src.user import update_user

    success = update_user(
        user["id"],
        name,
        email
    )

    if success:
        user = get_user(user["id"])
        print_success("Profile updated successfully.")

    else:
        print_error("Could not update profile.")

    pause()


# EXPENSE MANAGEMENT

def add_expense_menu(user):
    """Add a new expense."""

    clear_screen()
    print_logo()
    print_section("NEW EXPENSE")

    print()

    amount = get_valid_amount("  Amount ₹: ")

    category = choose_category()

    description = input("  Description: ").strip()

    expense_date = get_valid_date()

    expense_id = add_expense(
        user["id"],
        amount,
        category,
        description,
        expense_date
    )

    print()

    if expense_id:
        print_success("Expense added successfully!")
        print()
        print(f"  ID          : {expense_id}")
        print(f"  Amount      : {format_currency(amount)}")
        print(f"  Category    : {category}")
        print(f"  Description : {description}")
        print(f"  Date        : {expense_date}")

        # Check monthly budget
        month = expense_date[:7]

        status = get_budget_status(
            user["id"],
            month
        )

        if status:
            print()

            if status["remaining"] < 0:
                print_warning("Budget exceeded!")
                print_warning(
                    f"You are "
                    f"{format_currency(abs(status['remaining']))} "
                    f"over your budget."
                )

            elif status["remaining"] == 0:
                print_warning(
                    "You have reached your monthly budget."
                )

            elif status["budget"] > 0:
                percentage = (
                    status["spent"] /
                    status["budget"]
                ) * 100

                if percentage >= 80:
                    print_warning(
                        f"You have used {percentage:.0f}% "
                        "of your monthly budget."
                    )

    else:
        print_error("Could not add expense.")

    pause()


def display_expenses(expenses):
    """Display expenses in a formatted table."""

    if not expenses:
        print()
        print_info("No expenses found.")
        return

    print()

    print(
        "  "
        f"{'ID':<5}"
        f"{'Date':<14}"
        f"{'Category':<18}"
        f"{'Amount':>12}"
    )

    print("-" * 52)

    for expense in expenses:
        category = expense["category"][:17]

        print(
            "  "
            f"{expense['id']:<5}"
            f"{expense['expense_date']:<14}"
            f"{category:<18}"
            f"{format_currency(expense['amount']):>12}"
        )

        if expense["description"]:
            print(
                f"       {expense['description']}"
            )


def view_expenses(user):
    """Display all expenses."""

    clear_screen()
    print_logo()
    print_section("ALL EXPENSES")

    expenses = get_expenses(user["id"])

    display_expenses(expenses)

    if expenses:
        print()
        print(f"  Total records: {len(expenses)}")

    pause()


def search_expenses_menu(user):
    """Search expenses."""

    clear_screen()
    print_logo()
    print_section("SEARCH EXPENSES")

    print()

    keyword = input("  Search keyword: ").strip()

    if not keyword:
        print_error("Search keyword cannot be empty.")
        pause()
        return

    results = search_expenses(
        user["id"],
        keyword
    )

    print()
    print_info(
        f"Found {len(results)} matching expense(s)."
    )

    display_expenses(results)

    pause()


def edit_expense_menu(user):
    """Edit an existing expense."""

    clear_screen()
    print_logo()
    print_section("EDIT EXPENSE")

    expenses = get_expenses(user["id"])

    display_expenses(expenses)

    if not expenses:
        pause()
        return

    print()

    try:
        expense_id = int(
            input("  Enter expense ID: ").strip()
        )
    except ValueError:
        print_error("Invalid expense ID.")
        pause()
        return

    expense = get_expense(
        expense_id,
        user["id"]
    )

    if expense is None:
        print_error("Expense not found.")
        pause()
        return

    print()
    print_info("Press Enter to keep the existing value.")

    amount_input = input(
        f"  Amount [{expense['amount']}]: "
    ).strip()

    if amount_input:
        if not validate_amount(amount_input):
            print_error("Invalid amount.")
            pause()
            return

        amount = float(amount_input)
    else:
        amount = expense["amount"]

    category = input(
        f"  Category [{expense['category']}]: "
    ).strip()

    if not category:
        category = expense["category"]

    description = input(
        f"  Description [{expense['description'] or ''}]: "
    ).strip()

    if not description:
        description = expense["description"]

    expense_date = input(
        f"  Date [{expense['expense_date']}]: "
    ).strip()

    if not expense_date:
        expense_date = expense["expense_date"]

    if not validate_date(expense_date):
        print_error("Invalid date.")
        pause()
        return

    success = update_expense(
        expense_id,
        user["id"],
        amount,
        category,
        description,
        expense_date
    )

    if success:
        print()
        print_success("Expense updated successfully.")
    else:
        print_error("Could not update expense.")

    pause()


def delete_expense_menu(user):
    """Delete an expense."""

    clear_screen()
    print_logo()
    print_section("DELETE EXPENSE")

    expenses = get_expenses(user["id"])

    display_expenses(expenses)

    if not expenses:
        pause()
        return

    print()

    try:
        expense_id = int(
            input("  Enter expense ID to delete: ").strip()
        )
    except ValueError:
        print_error("Invalid expense ID.")
        pause()
        return

    expense = get_expense(
        expense_id,
        user["id"]
    )

    if expense is None:
        print_error("Expense not found.")
        pause()
        return

    print()
    print_warning(
        f"Delete {format_currency(expense['amount'])} "
        f"from {expense['category']}?"
    )

    confirmation = input(
        "  Type YES to confirm: "
    ).strip().upper()

    if confirmation != "YES":
        print_info("Deletion cancelled.")
        pause()
        return

    success = delete_expense(
        expense_id,
        user["id"]
    )

    if success:
        print_success("Expense deleted successfully.")
    else:
        print_error("Could not delete expense.")

    pause()


# BUDGET MANAGEMENT

def budget_menu(user):
    """Manage monthly budget."""

    while True:
        clear_screen()
        print_logo()
        print_section("BUDGET MANAGEMENT")

        month = get_current_month()

        status = get_budget_status(
            user["id"],
            month
        )

        print()
        print(f"  Current Month: {month}")

        if status:
            print()
            print(
                f"  Budget     : "
                f"{format_currency(status['budget'])}"
            )
            print(
                f"  Spent      : "
                f"{format_currency(status['spent'])}"
            )
            print(
                f"  Remaining  : "
                f"{format_currency(status['remaining'])}"
            )
            print(
                f"  Status     : "
                f"{status['status']}"
            )

            print()
            print(
                "  "
                + progress_bar(
                    status["spent"],
                    status["budget"]
                )
            )

        else:
            print()
            print_info("No budget has been set for this month.")

        print()
        print("  [1] Set / Update Budget")
        print("  [0] Back")

        choice = input("\n  Choose an option: ").strip()

        if choice == "1":
            amount = get_valid_amount(
                "  Enter monthly budget ₹: "
            )

            success = set_budget(
                user["id"],
                month,
                amount
            )

            if success:
                print_success(
                    f"Monthly budget set to "
                    f"{format_currency(amount)}."
                )
            else:
                print_error("Could not update budget.")

            pause()

        elif choice == "0":
            return

        else:
            print_error("Invalid option.")
            pause()


# ANALYTICS

def analytics_menu(user):
    """Display spending analytics."""

    clear_screen()
    print_logo()
    print_section("SPENDING ANALYTICS")

    total = get_total_expenses(user["id"])

    print()
    print(f"  Total Spending : {format_currency(total)}")

    categories = get_category_summary(user["id"])

    print()
    print("  CATEGORY BREAKDOWN")
    print("-" * 42)

    if categories:
        for category in categories:
            print(
                f"  {category['category']:<20}"
                f"{format_currency(category['total']):>15}"
            )
    else:
        print_info("No spending data available.")

    highest = get_highest_expense(user["id"])

    if highest:
        print()
        print("  HIGHEST EXPENSE")
        print("-" * 42)

        print(
            f"  Amount   : "
            f"{format_currency(highest['amount'])}"
        )
        print(
            f"  Category : {highest['category']}"
        )
        print(
            f"  Details  : "
            f"{highest['description'] or 'No description'}"
        )
        print(
            f"  Date     : {highest['expense_date']}"
        )

    month = get_current_month()

    monthly = get_monthly_summary(
        user["id"],
        month
    )

    print()
    print("  CURRENT MONTH")
    print("-" * 42)

    print(
        f"  Number of expenses : "
        f"{monthly['expense_count']}"
    )
    print(
        f"  Total spending     : "
        f"{format_currency(monthly['total'])}"
    )
    print(
        f"  Average expense    : "
        f"{format_currency(monthly['average'])}"
    )

    pause()


# DASHBOARD

def dashboard(user):
    """Main SpendWise dashboard."""

    while True:
        clear_screen()
        print_logo()

        month = get_current_month()

        status = get_budget_status(
            user["id"],
            month
        )

        total = get_total_expenses(
            user["id"]
        )

        print_section("DASHBOARD")

        print()
        print(f"  Student       : {user['name']}")
        print(
            f"  Current Month : {month}"
        )

        print_section("MONTHLY OVERVIEW")

        if status:
            budget = status["budget"]
            spent = status["spent"]
            remaining = status["remaining"]

            print()
            print(
                f"  Budget     : "
                f"{format_currency(budget)}"
            )
            print(
                f"  Spent      : "
                f"{format_currency(spent)}"
            )
            print(
                f"  Remaining  : "
                f"{format_currency(remaining)}"
            )

            print()
            print(
                "  "
                + progress_bar(spent, budget)
            )

            if remaining < 0:
                print_warning(
                    "You have exceeded your monthly budget!"
                )

            elif remaining == 0:
                print_warning(
                    "You have reached your monthly budget."
                )

        else:
            print()
            print_info(
                "No budget set for this month."
            )

        print_section("QUICK ACTIONS")

        print()
        print("  [1] Add Expense")
        print("  [2] View Expenses")
        print("  [3] Search Expenses")
        print("  [4] Edit Expense")
        print("  [5] Delete Expense")
        print("  [6] Budget Management")
        print("  [7] Analytics")
        print("  [8] Profile")
        print("  [0] Logout")

        print()
        print(f"  Total spending: {format_currency(total)}")

        choice = input(
            "\n  Choose an option: "
        ).strip()

        if choice == "1":
            add_expense_menu(user)

        elif choice == "2":
            view_expenses(user)

        elif choice == "3":
            search_expenses_menu(user)

        elif choice == "4":
            edit_expense_menu(user)

        elif choice == "5":
            delete_expense_menu(user)

        elif choice == "6":
            budget_menu(user)

        elif choice == "7":
            analytics_menu(user)

        elif choice == "8":
            profile_menu(user)

        elif choice == "0":
            print()
            print_info(
                f"Logged out. See you next time, {user['name']}!"
            )
            pause()
            return

        else:
            print_error("Invalid option.")
            pause()


# START SCREEN

def start_screen():
    """Display the application start screen."""

    initialize_database()

    while True:
        clear_screen()
        print_logo()

        print()
        print(
            "  Manage your student expenses."
        )
        print(
            "  Track spending. Set budgets. Understand your money."
        )

        print()
        print_section("GET STARTED")

        print()
        print("  [1] Create New Profile")
        print("  [2] Login")
        print("  [0] Exit")

        choice = input(
            "\n  Choose an option: "
        ).strip()

        if choice == "1":
            user = create_profile()

            if user:
                dashboard(user)

        elif choice == "2":
            user = login()

            if user:
                dashboard(user)

        elif choice == "0":
            clear_screen()
            print_logo()

            print()
            print(
                "  Thank you for using "
                "SpendWise."
            )
            print()
            break

        else:
            print_error("Invalid option.")
            pause()


if __name__ == "__main__":
    start_screen()
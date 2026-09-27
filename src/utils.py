CATEGORIES = [
    "Food",
    "Travel",
    "Education",
    "Shopping",
    "Entertainment",
    "Bills",
    "Health",
    "Other"
]


def clear_screen():
    """Leave some space before showing the next screen."""
    print("\n" * 2)


def print_logo():
    """Print a simple heading."""
    print()
    print("SpendWise")
    print("Student Expense Manager")
    print("-" * 30)


def print_section(title):
    """Print a section heading."""
    print()
    print(title)
    print("-" * len(title))


def print_success(message):
    print("Success:", message)


def print_error(message):
    print("Error:", message)


def print_warning(message):
    print("Warning:", message)


def print_info(message):
    print(message)


def format_currency(amount):
    """Show an amount in Indian rupees."""
    return f"Rs. {amount:,.2f}"


def progress_bar(value, maximum, width=20):
    """Show a small text-based budget indicator."""
    if maximum <= 0:
        return "[--------------------] 0%"

    percentage = min((value / maximum) * 100, 100)
    filled = int((percentage / 100) * width)
    bar = "#" * filled + "-" * (width - filled)

    return f"[{bar}] {percentage:.0f}%"


def pause():
    input("\nPress Enter to continue...")


def choose_category():
    """Ask the user to choose an expense category."""
    print_section("Expense Category")

    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("Choose a category: ").strip()

        try:
            choice = int(choice)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
        except ValueError:
            pass

        print_error("Please enter a valid category number.")

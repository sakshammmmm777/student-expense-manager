# SpendWise – Student Expense & Budget Management System

## 1. Project Overview

SpendWise is a simple command-line expense tracker I built for the Python Essentials course.  
It helps students record daily spending, set a monthly budget, and see where their money is going.

Everything runs offline using only the Python standard library and an SQLite database. No extra packages are needed.

---

## 2. Problem Statement

As a student I often spend money on food, travel, books and other things without writing it down.  
By the end of the month it is hard to know where the money went and whether I crossed my budget.

I wanted a lightweight tool that:
- works completely offline
- runs in the terminal
- saves data permanently
- still gives useful summaries

That is why I created SpendWise.

---

## 3. Objectives

* Record daily student expenses
* Organise expenses into categories
* Create and manage monthly budgets
* Search, edit and delete expense records
* Calculate total and category-wise spending
* Monitor monthly budget usage and show warnings
* Provide simple spending analytics
* Store data permanently using SQLite
* Apply input validation and basic error handling

---

## 4. Features

### User Management

* Create a user profile.
* Login using email.
* View profile information.
* Update profile information.

### Expense Management

* Add new expenses.
* View all expenses.
* Search expenses.
* Edit existing expenses.
* Delete expenses.
* Categorize expenses.

### Budget Management

* Set a monthly budget.
* Update an existing budget.
* View total monthly spending.
* Calculate remaining budget.
* Display budget status.
* Show warnings when spending approaches or exceeds the budget.

### Reports & Analytics

* Calculate total spending.
* Display category-wise spending.
* Find the highest expense.
* Generate monthly summaries.
* Calculate average expense amount.

### Database

* SQLite database for persistent storage.
* Separate tables for users, expenses, and budgets.
* CRUD operations for expense and profile management.

---

## 5. Technologies Used

* **Programming Language:** Python 3
* **Database:** SQLite
* **Interface:** Command Line Interface (CLI)
* **Version Control:** Git and GitHub
* **Libraries:** Python Standard Library

No external Python packages are required.

---

## 6. Project Structure

```text
student-expense-manager/
│
├── main.py
├── README.md
├── statement.md
├── requirements.txt
├── .gitignore
├── expenses.db
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── user.py
│   ├── expense.py
│   ├── budget.py
│   ├── reports.py
│   ├── validation.py
│   └── utils.py
│
├── tests/
│   ├── __init__.py
│   ├── test_expense.py
│   ├── test_budget.py
│   └── test_validation.py
│
└── docs/
```

---

## 7. Requirements

### Software Requirements

* Python 3.10 or above
* Windows, Linux, or macOS
* Command-line terminal
* Git (for GitHub submission)

### Dependencies

SpendWise uses only Python Standard Library modules.

No external packages are required.

---

## 8. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/sakshammmmm777/student-expense-manager.git
```

### Step 2: Open the project directory

```bash
cd student-expense-manager
```

### Step 3: Run the application

```bash
python main.py
```

The SQLite database is created automatically when the application starts.

---

## 9. Running the Project

From the project root directory:

```bash
python main.py
```

The application starts with the SpendWise welcome screen.

The user can then:

1. Create a profile or login.
2. Access the dashboard.
3. Add and manage expenses.
4. Set and monitor a monthly budget.
5. View analytics.
6. Logout.

---

## 10. Expense Categories

The application provides the following categories:

* Food
* Travel
* Education
* Shopping
* Entertainment
* Bills
* Health
* Other

---

## 11. Budget Monitoring

Users can set a monthly budget.

SpendWise calculates:

```text
Remaining Budget = Monthly Budget - Total Monthly Spending
```

The application shows a warning when the budget has been reached or exceeded.

---

## 12. Database Design

The application uses three main SQLite tables.

### Users

Stores student profile information.

```text
id
name
email
```

### Expenses

Stores individual expense records.

```text
id
user_id
amount
category
description
expense_date
```

### Budgets

Stores monthly budget information.

```text
id
user_id
month
amount
```

The `user_id` field connects expenses and budgets to the corresponding user.

---

## 13. Input Validation

SpendWise validates user input before storing data.

Validation includes:

* Name validation
* Email validation
* Positive amount validation
* Date validation
* Expense category selection
* Invalid menu input handling

This helps prevent incorrect or invalid records.

---

## 14. Testing

The project includes test files for important functionality:

```text
tests/
├── test_expense.py
├── test_budget.py
└── test_validation.py
```

The application was also manually tested through the command line for:

* Profile creation
* Login
* Expense addition
* Expense search
* Expense editing
* Expense deletion
* Budget creation
* Budget monitoring
* Analytics

---

## 15. Future Enhancements

Possible future improvements include:

* Graphical user interface.
* Data visualization and charts.
* Export reports to CSV or PDF.
* Recurring expense support.
* Savings goal tracking.
* Password-based authentication.
* Advanced financial insights.
* Mobile or web-based version.

---

## 16. Conclusion

SpendWise is my attempt to solve a real problem I face every month – tracking expenses without complicated apps.  
While building it I practised functions, modules, SQLite, validation, exception handling and a clean menu-driven CLI.

The project can be run with Python's standard library and SQLite.

---

## 17. Author

**Project:** SpendWise – Student Expense & Budget Management System  
**Course:** Python Essentials  
**Student:** Saksham Dwivedi  
**Registration No.:** 26BCE11569  
**GitHub:** https://github.com/sakshammmmm777/student-expense-manager

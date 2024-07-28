# Expense Management App

This is an expense management application built with Flask. It allows users to create accounts, add expenses, and generate balance sheets.

## Features

- Create user accounts
- Add expenses
- View expenses by user
- Generate and download balance sheets as CSV files

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/expense_app.git
    cd expense_app
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Run the application:**

    ```sh
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Users

- **Create a user:**

    ```http
    POST /users
    ```

    **Request body:**

    ```json
    {
        "email": "user@example.com",
        "name": "John Doe",
        "mobile_number": "1234567890"
    }
    ```

    **Response:**

    ```json
    {
        "message": "User created successfully",
        "user_id": 1
    }
    ```

- **Get a user:**

    ```http
    GET /users/<user_id>
    ```

    **Response:**

    ```json
    {
        "email": "user@example.com",
        "name": "John Doe",
        "mobile_number": "1234567890"
    }
    ```

### Expenses

- **Add an expense:**

    ```http
    POST /expenses
    ```

    **Request body:**

    ```json
    {
        "amount": 100.0,
        "paid_by": 1,
        "description": "Dinner",
        "splits": [
            {"user_id": 1, "amount": 50.0},
            {"user_id": 2, "amount": 50.0}
        ]
    }
    ```

    **Response:**

    ```json
    {
        "message": "Expense added successfully",
        "expense_id": 1
    }
    ```

- **Get expenses by user:**

    ```http
    GET /expenses/user/<user_id>
    ```

    **Response:**

    ```json
    [
        {
            "id": 1,
            "amount": 100.0,
            "description": "Dinner",
            "paid_by_user_id": 1
        }
    ]
    ```

- **Get all expenses:**

    ```http
    GET /expenses
    ```

    **Response:**

    ```json
    [
        {
            "id": 1,
            "amount": 100.0,
            "description": "Dinner",
            "paid_by_user_id": 1
        }
    ]
    ```

### Balance Sheet

- **Download balance sheet:**

    ```http
    GET /balance_sheet
    ```

    **Response:**

    A CSV file containing the balance sheet data.


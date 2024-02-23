# ExpenseTracker Project

## Overview

ExpenseTracker is a simple expense tracking application built using Python and the Tkinter library for the graphical user interface. It leverages MongoDB as the backend database for storing expense data. The project is organized into several modules to manage the input, display, and manipulation of expenses.

## Features

- **Expense Input Frame:** Allows users to input expense details, including category and amount, and adds them to the expense list.
- **Expense Listbox:** Displays a list of expenses, allowing users to delete and edit existing expenses.
- **MongoDB Integration:** Stores expense data in a MongoDB database for persistent storage.

## Frameworks/Libraries Used

- **Tkinter:** Used for building the graphical user interface.
- **MongoDB:** Provides the backend database for storing and managing expense data.

## How to Run

1. Ensure you have Python installed on your machine.
2. Install the required dependencies by running:

    ```bash
    pip install pymongo
    ```

3. Run the main script:

    ```bash
    python main.py
    ```

## Project Structure

The project is organized into the following modules:

- **main.py:** Entry point of the application.
- **expense_tracker_app.py:** Defines the `ExpenseTrackerApp` class, responsible for managing the overall application.
- **expense_input_frame.py:** Contains the `ExpenseInputFrame` class, handling the input of new expenses.
- **expense_listbox.py:** Implements the `ExpenseListbox` class, responsible for displaying and managing the list of expenses.

## Contributions

Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## About the Author

### Frederico Fernandes

Connect with me on [LinkedIn](https://www.linkedin.com/in/f-fernandes/)!

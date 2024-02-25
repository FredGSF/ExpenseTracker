import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
import datetime
from expense_listbox import ExpenseListbox
from expense_input_frame import ExpenseInputFrame


# Creating a class for the Expense Tracker App
class ExpenseTrackerApp:
    def __init__(self, root):
        # Initializing the main window and setting its title
        self.root = root
        self.root.title("Expense Tracker")
        # Connecting to MongoDB and creating widgets
        self.connect_to_mongodb()
        self.create_widgets()

    # Method to connect to MongoDB
    def connect_to_mongodb(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["expense_tracker_db"]
        self.expenses_collection = self.database["expenses"]

    # Method to create widgets (input frame and listbox)
    def create_widgets(self):
        # Creating and initializing ExpenseInputFrame
        input_frame = ExpenseInputFrame(
            self.root,
            self.add_expense,
            self.update_expense_listbox,
            self.expenses_collection,
        )

        # Creating and initializing ExpenseListbox
        self.listbox = ExpenseListbox(
            self.root,
            self.delete_expense,
            self.edit_expense,
            self.update_expense_listbox,
            self.expenses_collection,
        )

    # Method to add an expense to MongoDB and update the Listbox
    def add_expense(self, category, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            self.show_error_message(str(e))
            return

        expense = {
            "category": category,
            "amount": amount,
            "timestamp": datetime.datetime.now(),
        }

        # Insert expense into MongoDB
        self.expenses_collection.insert_one(expense)
        # Update the Listbox
        self.update_expense_listbox()
        # Clear entry fields
        self.clear_entry_fields()

    def delete_expense(self, expense_id):
        # Delete expense from MongoDB
        result = self.expenses_collection.delete_one({"_id": expense_id})

        if result.deleted_count == 1:
            # Update the Listbox
            self.update_expense_listbox()
        else:
            self.show_error_message("Failed to delete expense.")

    def edit_expense(self, expense_id, new_category, new_amount):
        # Retrieve the selected expense
        selected_expense = self.expenses_collection.find_one({"_id": expense_id})

        if not selected_expense:
            self.show_error_message("Expense not found.")
            return

        try:
            new_amount = float(new_amount)
            if new_amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            self.show_error_message(str(e))
            return

        updated_expense = {
            "category": new_category,
            "amount": new_amount,
            "timestamp": datetime.datetime.now(),
        }

        # Update expense in MongoDB
        result = self.expenses_collection.update_one(
            {"_id": expense_id}, {"$set": updated_expense}
        )

        if result.modified_count == 1:
            # Update the Listbox
            self.update_expense_listbox()
        else:
            self.show_error_message("Failed to edit expense.")

    def update_expense_listbox(self):
        # Retrieve expenses from MongoDB and update the Listbox
        self.listbox.update_listbox()

    def clear_entry_fields(self):
        # ToDo
        # need to implement
        pass

    # Method to display an error message using a tkinter messagebox
    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # Method to close the MongoDB connection and destroy the main window
    def close_app(self):
        self.client.close()
        self.root.destroy()

    # Method to run the application
    def run(self):
        # Set a protocol to handle window close event and start the main loop
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()


# Main block to create a tkinter root window and instantiate the ExpenseTrackerApp
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    app.run()

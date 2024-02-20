import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
import datetime
from expense_listbox import ExpenseListbox
from expense_input_frame import ExpenseInputFrame


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.connect_to_mongodb()
        self.create_widgets()

    def connect_to_mongodb(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["expense_tracker_db"]
        self.expenses_collection = self.database["expenses"]

    def create_widgets(self):
        ExpenseInputFrame(self.root, self.add_expense, self.update_expense_listbox)
        ExpenseListbox(
            self.root,
            self.delete_expense,
            self.edit_expense,
            self.update_expense_listbox,
        )

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
        self.listbox_expenses.delete(0, tk.END)
        for expense in self.expenses_collection.find():
            display_text = (
                f"{expense.get('category', '')}: ${expense.get('amount', 0):.2f}"
            )
            if "timestamp" in expense:
                display_text += f" - {expense['timestamp']}"
            self.listbox_expenses.insert(tk.END, display_text)

    def close_app(self):
        self.client.close()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

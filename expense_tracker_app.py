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
        ExpenseListbox(self.root, self.delete_expense, self.edit_expense, self.update_expense_listbox)

    def add_expense(self, category, amount):
        # Implement add_expense logic here

    def delete_expense(self, expense_id):
        # Implement delete_expense logic here

    def edit_expense(self, expense_id, new_category, new_amount):
        # Implement edit_expense logic here

    def update_expense_listbox(self):
        # Implement update_expense_listbox logic here

    def close_app(self):
        self.client.close()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import pymongo
import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["expense_tracker_db"]
        self.expenses_collection = self.database["expenses"]

        # Widgets
        self.frame_input = ttk.Frame(root)
        self.frame_input.pack(pady=10)

        self.label_category = ttk.Label(self.frame_input, text="Category:")
        self.entry_category = ttk.Entry(self.frame_input)

        self.label_amount = ttk.Label(self.frame_input, text="Amount:")
        self.entry_amount = ttk.Entry(self.frame_input)

        self.button_add_expense = ttk.Button(
            root, text="Add Expense", command=self.add_expense
        )

        # Buttons for delete and edit
        self.button_delete_expense = ttk.Button(
            root, text="Delete Expense", command=self.delete_expense
        )
        self.button_edit_expense = ttk.Button(
            root, text="Edit Expense", command=self.edit_expense
        )

        # Listbox to display expenses
        self.listbox_expenses = tk.Listbox(root)
        self.listbox_expenses.pack()

        # Pack widgets
        self.label_category.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_category.grid(row=0, column=1, padx=5, pady=5)

        self.label_amount.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)

        self.button_add_expense.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_delete_expense.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_edit_expense.grid(row=4, column=0, columnspan=2, pady=10)

        # Populate the Listbox
        self.update_expense_listbox()

    def add_expense(self):
        category = self.entry_category.get()
        amount = self.entry_amount.get()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
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
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def delete_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select an expense to delete.")
            return

        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        self.expenses_collection.delete_one({"_id": expense_id})

        # Update the Listbox
        self.update_expense_listbox()

    def edit_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select an expense to edit.")
            return

        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        # Implement editing functionality as per your requirement

    def update_expense_listbox(self):
        # Retrieve expenses from MongoDB and update the Listbox
        self.listbox_expenses.delete(0, tk.END)
        for expense in self.expenses_collection.find():
            display_text = f"{expense['category']}: ${expense['amount']:.2f} - {expense['timestamp']}"
            self.listbox_expenses.insert(tk.END, display_text)

    def close_app(self):
        self.client.close()
        self.root.destroy()

    def run(self):
        self.root.protocol(
            "WM_DELETE_WINDOW", self.close_app
        )  # Handle window close event
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    app.run()

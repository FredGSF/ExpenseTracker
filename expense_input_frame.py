import tkinter as tk
from tkinter import ttk, messagebox


class ExpenseInputFrame:
    def __init__(
        self, parent, add_expense_callback, update_listbox_callback, expenses_collection
    ):
        self.parent = parent
        self.add_expense_callback = add_expense_callback
        self.update_listbox_callback = update_listbox_callback
        self.expenses_collection = expenses_collection
        self.create_input_frame()

    def create_input_frame(self):
        self.frame_input = ttk.Frame(self.parent)
        self.frame_input.grid(row=0, column=0, padx=60, pady=20, sticky=tk.W)

        self.label_category = ttk.Label(self.frame_input, text="Category:")
        self.entry_category = ttk.Entry(self.frame_input)

        self.label_amount = ttk.Label(self.frame_input, text="Amount:")
        self.entry_amount = ttk.Entry(self.frame_input)

        self.button_add_expense = ttk.Button(
            self.frame_input, text="Add Expense", command=self.add_expense
        )

        self.label_category.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_category.grid(row=0, column=1, padx=5, pady=5)
        self.label_amount.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)
        self.button_add_expense.grid(row=2, column=0, columnspan=2, pady=10)

    def add_expense(self):
        category = self.entry_category.get()
        amount = self.entry_amount.get()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            self.show_error_message(str(e))
            return

        self.add_expense_callback(category, amount)
        self.update_listbox_callback()
        self.clear_entry_fields()

    def clear_entry_fields(self):
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

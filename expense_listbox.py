import tkinter as tk
from tkinter import ttk, messagebox
import datetime


class ExpenseListbox:
    def __init__(
        self,
        parent,
        delete_callback,
        edit_callback,
        update_listbox_callback,
        expenses_collection,
    ):
        self.parent = parent
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.update_listbox_callback = update_listbox_callback
        self.expenses_collection = expenses_collection
        self.create_expenses_listbox()
        self.update_listbox()

    def create_expenses_listbox(self):
        self.listbox_expenses = tk.Listbox(self.parent)
        self.listbox_expenses.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    def delete_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            self.show_info_message("Please select an expense to delete.")
            return

        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        self.delete_callback(expense_id)
        self.update_listbox_callback()

    def edit_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            self.show_info_message("Please select an expense to edit.")
            return

        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        selected_expense = self.expenses_collection.find_one({"_id": expense_id})

        # Create a new window for editing
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Edit Expense")

        label_category = ttk.Label(edit_window, text="Category:")
        entry_category = ttk.Entry(edit_window)
        label_category.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        entry_category.grid(row=0, column=1, padx=5, pady=5)
        entry_category.insert(0, selected_expense.get("category", ""))

        label_amount = ttk.Label(edit_window, text="Amount:")
        entry_amount = ttk.Entry(edit_window)
        label_amount.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        entry_amount.grid(row=1, column=1, padx=5, pady=5)
        entry_amount.insert(0, selected_expense.get("amount", ""))

        button_save = ttk.Button(
            edit_window,
            text="Save Changes",
            command=lambda: self.save_changes(
                edit_window, expense_id, entry_category.get(), entry_amount.get()
            ),
        )
        button_save.grid(row=2, column=0, columnspan=2, pady=10)

    def save_changes(self, edit_window, expense_id, new_category, new_amount):
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
            self.update_listbox_callback()
            # Close the edit window
            edit_window.destroy()
        else:
            self.show_error_message("Failed to save changes.")

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_info_message(self, message):
        messagebox.showinfo("Info", message)

    def update_listbox(self):
        # Retrieve expenses from MongoDB and update the Listbox
        self.listbox_expenses.delete(0, tk.END)
        for expense in self.expenses_collection.find():
            display_text = (
                f"{expense.get('category', '')}: ${expense.get('amount', 0):.2f}"
            )
            if "timestamp" in expense:
                display_text += f" - {expense['timestamp']}"
            self.listbox_expenses.insert(tk.END, display_text)


if __name__ == "__main__":
    root = tk.Tk()
    listbox = ExpenseListbox(root, None, None, None, None)
    root.mainloop()

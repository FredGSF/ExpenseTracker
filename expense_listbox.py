import tkinter as tk
from tkinter import ttk, messagebox
import datetime


# Creating a class for the Expense Listbox
class ExpenseListbox:
    def __init__(
        self,
        parent,
        delete_callback,
        edit_callback,
        update_listbox_callback,
        expenses_collection,
    ):
        # Initializing instance variables with provided parameters
        self.parent = parent
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.update_listbox_callback = update_listbox_callback
        self.expenses_collection = expenses_collection
        self.create_expenses_listbox()
        self.update_listbox()

    # Method to create the expenses listbox
    def create_expenses_listbox(self):
        # Creating a tkinter Listbox within the specified parent
        self.listbox_expenses = tk.Listbox(self.parent)
        self.listbox_expenses.grid(row=1, column=0, padx=30, pady=30, sticky=tk.W)

    # Method to delete the selected expense
    def delete_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            # Getting the selected index from the listbox
            self.show_info_message("Please select an expense to delete.")
            return

        # Retrieving the expense ID from the MongoDB collection based on the selected index
        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        # Calling the provided delete callback and updating the listbox
        self.delete_callback(expense_id)
        self.update_listbox_callback()

    # Method to edit the selected expense
    def edit_expense(self):
        # Getting the selected index from the listbox
        selected_index = self.listbox_expenses.curselection()
        if not selected_index:
            # Displaying an info message if no expense is selected
            self.show_info_message("Please select an expense to edit.")
            return

        # Retrieving the expense ID and details from MongoDB based on the selected index
        expense_id = self.expenses_collection.find()[selected_index[0]]["_id"]
        selected_expense = self.expenses_collection.find_one({"_id": expense_id})

        # Create a new window for editing
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Edit Expense")

        # Creating labels and entry fields for category and amount in the edit window
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

        # Creating a button to save changes, associating it with the save_changes method
        button_save = ttk.Button(
            edit_window,
            text="Save Changes",
            command=lambda: self.save_changes(
                edit_window, expense_id, entry_category.get(), entry_amount.get()
            ),
        )
        button_save.grid(row=2, column=0, columnspan=2, pady=10)

    # Method to save changes made in the edit window
    def save_changes(self, edit_window, expense_id, new_category, new_amount):
        # Validating the new amount as a positive float
        try:
            new_amount = float(new_amount)
            if new_amount <= 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError as e:
            self.show_error_message(str(e))
            return
        # Creating an updated expense dictionary with new values and timestamp
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
            # Displaying an error message if the update fails
            self.show_error_message("Failed to save changes.")

    # Method to display an error message using a tkinter messagebox
    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # Method to display an info message using a tkinter messagebox
    def show_info_message(self, message):
        messagebox.showinfo("Info", message)

    # Method to update the Listbox with the latest data from MongoDB
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


# Main block to create a tkinter root window and instantiate the ExpenseListbox
if __name__ == "__main__":
    root = tk.Tk()
    listbox = ExpenseListbox(root, None, None, None, None)
    root.mainloop()

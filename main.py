import tkinter as tk
from expense_tracker_app import ExpenseTrackerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    app.run()

import pandas as pd
from django.shortcuts import render
from .models import Expense


def expense_list(request):
    expenses = Expense.objects.all()

    # Use pandas to analyze data
    df = pd.DataFrame(list(expenses.values()))
    total_expenses_per_category = (
        df.groupby("category_id")["amount"].sum().reset_index()
    )

    return render(
        request,
        "expenses/expense_list.html",
        {
            "expenses": expenses,
            "total_expenses_per_category": total_expenses_per_category,
        },
    )


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "expenses/add_expense.html", {"form": form})

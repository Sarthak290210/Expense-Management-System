from fastapi import FastAPI
from datetime import datetime
from datetime import date
from Backend import db_helper
from typing import List
from pydantic import BaseModel


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


app = FastAPI()

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses_by_date(expense_date: date):
    expenses = db_helper.fetch_expenses_by_date(expense_date)
    return expenses

@app.post("/expenses/{expense_date}")
def add_update_expenses(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expenses_by_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses added/updated successfully."}

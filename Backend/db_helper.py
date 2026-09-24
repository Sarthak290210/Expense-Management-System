import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv
from pathlib import Path
import os
from Backend import logging_setup

load_dotenv()
logger = logging_setup.setup_logging("DBHelper")


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()
    
def fetch_expenses_by_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_db_cursor() as cursor:
        query = "SELECT * FROM expenses WHERE expense_date = %s"
        cursor.execute(query, (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def delete_expenses_by_date(expense_date):
    logger.info(f"Deleting expenses for date: {expense_date}")
    with get_db_cursor(commit = True) as cursor:
        query = "DELETE FROM expenses WHERE expense_date = %s"
        cursor.execute(query, (expense_date,))
        
def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense: Date: {expense_date}, Amount: {amount}, Category: {category}, Notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (expense_date, amount, category, notes))
        
def fetch_expenses_summary(start_date, end_date):
    logger.info(f"Fetching expenses summary from {start_date} to {end_date}")
    with get_db_cursor() as cursor:
        query = """
            SELECT Category, SUM(amount) AS total_amount
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY Category
            order by total_amount DESC
        """
        cursor.execute(query, (start_date, end_date))
        summary = cursor.fetchall()
        return summary
        
if __name__ == "__main__":
    expenses =fetch_expenses_by_date('2024-09-30')
    for expense in expenses:
        print(f"Date: {expense['expense_date']}, Amount: {expense['amount']}, Category: {expense['category']}, Notes: {expense['notes']}")
    print("*"*20)
    expenses_1 = fetch_expenses_summary('2024-09-01', '2024-09-30')
    for expense in expenses_1:
        print(f"Category: {expense['Category']}, Total Amount: {expense['total_amount']}")
    
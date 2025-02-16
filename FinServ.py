import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Define the file where transactions will be stored
FILE_NAME = "finance_data.csv"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Type", "Amount"])
    df.to_csv(FILE_NAME, index=False)

# Function to add a transaction
def add_transaction():
    date = date_entry.get()
    category = category_entry.get()
    trans_type = type_var.get()
    amount = amount_entry.get()
    
    if not date or not category or not trans_type or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return
    
    new_data = pd.DataFrame([[date, category, trans_type, amount]], columns=["Date", "Category", "Type", "Amount"])
    df = pd.read_csv(FILE_NAME)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    messagebox.showinfo("Success", "Transaction added successfully!")

# Function to generate summary
def generate_summary():
    df = pd.read_csv(FILE_NAME)
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    savings = income - expense
    messagebox.showinfo("Summary", f"Total Income: ${income}\nTotal Expenses: ${expense}\nNet Savings: ${savings}")

# Function to generate a pie chart of expenses
def plot_expenses():
    df = pd.read_csv(FILE_NAME)
    expense_df = df[df["Type"] == "Expense"]
    if expense_df.empty:
        messagebox.showinfo("Info", "No expenses recorded yet!")
        return
    expense_summary = expense_df.groupby("Category")["Amount"].sum()
    expense_summary.plot(kind="pie", autopct='%1.1f%%')
    plt.title("Expense Distribution by Category")
    plt.show()

# Function to generate income vs expense bar chart
def plot_income_vs_expense():
    df = pd.read_csv(FILE_NAME)
    summary = df.groupby("Type")["Amount"].sum()
    summary.plot(kind="bar", color=["green", "red"])
    plt.title("Income vs Expenses")
    plt.ylabel("Amount ($)")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("400x400")

# Input Fields
tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Type:").pack()
type_var = tk.StringVar(value="Income")
tk.Radiobutton(root, text="Income", variable=type_var, value="Income").pack()
tk.Radiobutton(root, text="Expense", variable=type_var, value="Expense").pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Buttons
tk.Button(root, text="Add Transaction", command=add_transaction).pack()
tk.Button(root, text="Generate Summary", command=generate_summary).pack()
tk.Button(root, text="Show Expense Distribution", command=plot_expenses).pack()
tk.Button(root, text="Show Income vs Expenses", command=plot_income_vs_expense).pack()
tk.Button(root, text="Exit", command=root.quit).pack()

# Run the application
root.mainloop()

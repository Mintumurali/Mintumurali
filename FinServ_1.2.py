import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

# Define the file where transactions will be stored
FILE_NAME = "finance_data.csv"
BUDGET_FILE = "budget.json"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Type", "Amount"])
    df.to_csv(FILE_NAME, index=False)

if not os.path.exists(BUDGET_FILE):
    with open(BUDGET_FILE, "w") as f:
        json.dump({"budget": 1000}, f)  # Default budget value

# Function to toggle dark mode
def toggle_dark_mode():
    bg_color = "#2E2E2E" if root.cget("bg") == "#F0F0F0" else "#F0F0F0"
    fg_color = "white" if bg_color == "#2E2E2E" else "black"
    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        widget.configure(bg=bg_color, fg=fg_color)

# Function to set budget
def set_budget():
    new_budget = budget_entry.get()
    try:
        new_budget = float(new_budget)
        with open(BUDGET_FILE, "w") as f:
            json.dump({"budget": new_budget}, f)
        messagebox.showinfo("Success", "Budget updated successfully!")
        update_budget_display()
    except ValueError:
        messagebox.showerror("Error", "Budget must be a number!")

# Function to update budget display
def update_budget_display():
    with open(BUDGET_FILE, "r") as f:
        budget_data = json.load(f)
    budget_label.config(text=f"Budget: ${budget_data['budget']}")

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
    update_transaction_list()

# Function to update transaction list
def update_transaction_list():
    df = pd.read_csv(FILE_NAME)
    transaction_list.delete(*transaction_list.get_children())
    for _, row in df.iterrows():
        transaction_list.insert("", "end", values=list(row))

# GUI Setup
root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("600x500")

# Budget Display
budget_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
budget_label.pack()
update_budget_display()

tk.Label(root, text="Set Budget:").pack()
budget_entry = tk.Entry(root)
budget_entry.pack()
tk.Button(root, text="Update Budget", command=set_budget).pack()

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
tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode).pack()
tk.Button(root, text="Exit", command=root.quit).pack()

# Transaction List
transaction_list = ttk.Treeview(root, columns=("Date", "Category", "Type", "Amount"), show="headings")
transaction_list.heading("Date", text="Date")
transaction_list.heading("Category", text="Category")
transaction_list.heading("Type", text="Type")
transaction_list.heading("Amount", text="Amount")
transaction_list.pack()

update_transaction_list()

# Run the application
root.mainloop()

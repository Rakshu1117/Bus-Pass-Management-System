import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Data for places
PLACES = {
    "bangalore": 0, "mysore": 145, "hubli": 413, "mangalore": 350,
    "udupi": 407, "belgaum": 504, "coorg": 250, "chikmagalur": 245,
    "dharwad": 419, "tumkur": 70
}

# In-memory storage of users
users = {}

class User:
    def __init__(self, card_id, holder_name):
        self.card_id = card_id
        self.holder_name = holder_name

class BusPass(User):
    def __init__(self, card_id, holder_name, balance):
        super().__init__(card_id, holder_name)  # Inherit properties from User
        self.balance = balance
        self.history = []

    def add_funds(self, amount):
        if amount <= 0:
            return {"error": "Amount must be positive!"}
        self.balance += amount
        return {"message": f"Added ₹{amount}. Current balance: ₹{self.balance}"}

    def deduct_fare(self, start_location, destination):
        fare = self.calculate_fare(start_location, destination)
        if fare is None:
            return {"error": "Invalid locations!"}
        if self.balance < fare:
            return {"error": "Insufficient balance!"}
        self.balance -= fare
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {start_location.capitalize()} → {destination.capitalize()} | Fare: ₹{fare}")
        return {"message": f"Fare ₹{fare} deducted. Remaining balance: ₹{self.balance}"}

    def calculate_fare(self, start_location, destination):
        if start_location not in PLACES or destination not in PLACES:
            return None
        distance = abs(PLACES[start_location] - PLACES[destination])
        return ((distance + 4) // 5) * 10  # ₹10 per 5 km

    def get_balance(self):
        return {"message": f"Current balance: ₹{self.balance}"}

    def get_history(self):
        if not self.history:
            return {"message": "No travel history found."}
        return {"message": "\n".join(self.history)}

# Tkinter GUI
def start_gui():
    def register():
        card_id, name, balance = entry_card_id.get(), entry_name.get(), entry_balance.get()
        try:
            balance = float(balance)
            if card_id in users:
                messagebox.showerror("Error", "Card ID already exists!")
            else:
                users[card_id] = BusPass(card_id, name, balance)
                messagebox.showinfo("Registration", "User registered successfully!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid balance!")

    def add_funds():
        card_id, amount = entry_card_id.get(), entry_funds.get()
        try:
            amount = float(amount)
            user = users.get(card_id)
            if user:
                response = user.add_funds(amount)
                messagebox.showinfo("Add Funds", response.get("message", response.get("error")))
            else:
                messagebox.showerror("Error", "User not found!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    def deduct_fare():
        card_id = entry_card_id.get()
        start, destination = start_var.get(), destination_var.get()
        user = users.get(card_id)
        if user:
            response = user.deduct_fare(start, destination)
            messagebox.showinfo("Deduct Fare", response.get("message", response.get("error")))
        else:
            messagebox.showerror("Error", "User not found!")

    def view_balance():
        card_id = entry_card_id.get()
        user = users.get(card_id)
        if user:
            response = user.get_balance()
            messagebox.showinfo("Balance", response["message"])
        else:
            messagebox.showerror("Error", "User not found!")

    def view_history():
        card_id = entry_card_id.get()
        user = users.get(card_id)
        if user:
            response = user.get_history()
            messagebox.showinfo("Travel History", response["message"])
        else:
            messagebox.showerror("Error", "User not found!")

    root = tk.Tk()
    root.title("Smart Bus Pass")

    tk.Label(root, text="Card ID:").grid(row=0, column=0)
    entry_card_id = tk.Entry(root)
    entry_card_id.grid(row=0, column=1)

    tk.Label(root, text="Name:").grid(row=1, column=0)
    entry_name = tk.Entry(root)
    entry_name.grid(row=1, column=1)

    tk.Label(root, text="Initial Balance:").grid(row=2, column=0)
    entry_balance = tk.Entry(root)
    entry_balance.grid(row=2, column=1)

    tk.Button(root, text="Register", command=register).grid(row=3, column=0, columnspan=2)

    tk.Label(root, text="Amount:").grid(row=4, column=0)
    entry_funds = tk.Entry(root)
    entry_funds.grid(row=4, column=1)

    tk.Button(root, text="Add Funds", command=add_funds).grid(row=5, column=0, columnspan=2)

    tk.Label(root, text="Start:").grid(row=6, column=0)
    start_var = tk.StringVar(root)
    ttk.Combobox(root, textvariable=start_var, values=list(PLACES.keys())).grid(row=6, column=1)

    tk.Label(root, text="Destination:").grid(row=7, column=0)
    destination_var = tk.StringVar(root)
    ttk.Combobox(root, textvariable=destination_var, values=list(PLACES.keys())).grid(row=7, column=1)

    tk.Button(root, text="Deduct Fare", command=deduct_fare).grid(row=8, column=0, columnspan=2)
    tk.Button(root, text="View Balance", command=view_balance).grid(row=9, column=0, columnspan=2)
    tk.Button(root, text="View Travel History", command=view_history).grid(row=10, column=0, columnspan=2)
    tk.Button(root, text="Exit", command=root.destroy).grid(row=11, column=0, columnspan=2)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    start_gui()

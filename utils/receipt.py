
import datetime
from routes.user import User


def deposit_receipt(account_number, amount, previous_balance=None):
    for user in User.load_users():
        if user["account_number"] == account_number:
            if previous_balance is None:
                previous_balance = user["balance"] - amount
            new_balance = user["balance"]
            receipt = f"""
            ────────────────────────────────
            HIFADHI BANK
            DEPOSIT RECEIPT
            ────────────────────────────────
            Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Account Number: {user["account_number"]}
            Name: {user["name"]}
            Email: {user["email"]}
            previous Balance: ${previous_balance:.2f}
            amount Deposited: ${amount:.2f}
            New Balance: ${new_balance:.2f}
            ────────────────────────────────
            """
            return receipt
    return "Account not found."

def withdraw_receipt(account_number, amount, previous_balance=None):
    for user in User.load_users():
        if user["account_number"] == account_number:
            if previous_balance is None:
                previous_balance = user["balance"] + amount
            new_balance = user["balance"]
            receipt = f"""
            ────────────────────────────────
            HIFADHI BANK
            DEPOSIT RECEIPT
            ────────────────────────────────
            Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Account Number: {user["account_number"]}
            Name: {user["name"]}
            Email: {user["email"]}
            previous Balance: ${previous_balance:.2f}
            amount Withdrawn: ${amount:.2f}
            New Balance: ${new_balance:.2f}
            ────────────────────────────────
            """
            return receipt
    return "Account not found."
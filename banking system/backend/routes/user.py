import json
import random
import hashlib
from pathlib import Path

class User:
    next_id = 1
    FILE = Path(__file__).resolve().parent.parent / "data" / "users.json"

    def __init__(self, name, email, user_id=None, set_pin=None, balance=0, card_number=None):
        if user_id is None:
            self.user_id = User.next_id
            User.next_id += 1
        else:
            self.user_id = user_id

        self.name = name
        self.email = email
        self.balance = balance
        self.card_number = card_number
        # PIN hashing
        self.set_pin = hashlib.sha256(set_pin.encode()).hexdigest()

    # Generate a unique account number
    @classmethod
    def account_assigner(cls):
        users = cls.load_users()

        existing_accounts = {
            user["account_number"]
            for user in users
        }

        while True:
            account_number = random.randint(1000, 9999)

            if account_number not in existing_accounts:
                return account_number
    #virtual card
    @classmethod
    def card_assigner(cls):
        users = cls.load_users()

        existing_cards = {
            user.get("card_number")
            for user in users
        }

        while True:
            card_number = random.randint(111111, 999999)

            if card_number not in existing_cards:
                return card_number

    # Save user to JSON
    def admin(self):
        users = User.load_users()

        user_data = {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "account_number": self.account_assigner(),
            "set_pin": self.set_pin,
            "balance": self.balance,
            "card_number": self.card_number or self.card_assigner()
        }

        users.append(user_data)

        with open(User.FILE, "w") as file:
            json.dump(users, file, indent=4)

    # Load users from JSON
    @classmethod
    def load_users(cls):
        try:
            with open(cls.FILE, "r") as file:
                users = json.load(file)
                if not isinstance(users, list):
                    return []
                return users

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Authenticate user using card number and PIN
    @classmethod
    def authenticate(cls, card_number, pin):
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        card_number = str(card_number)

        users = cls.load_users()

        return next(
            (
                user
                for user in users
                if user.get("card_number") is not None
                and str(user["card_number"]) == card_number
                and user["set_pin"] == hashed_pin
            ),
            None
        )
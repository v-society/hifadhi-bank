from routes.user import User

def deposit(account_number, amount):
    if amount <= 0:
        return False

    users = User.load_users()
    for user in users:
        if user["account_number"] == account_number:
            user["balance"] += amount
            with open(User.FILE, "w") as file:
                import json
                json.dump(users, file, indent=4)
            return True
    return False

def withdraw(account_number, amount):
    if amount <= 0:
        return False

    users = User.load_users()
    for user in users:
        if user["account_number"] == account_number:
            if user["balance"] >= amount:
                user["balance"] -= amount
                with open(User.FILE, "w") as file:
                    import json
                    json.dump(users, file, indent=4)
                return True
            else:
                print("Insufficient funds.")
                return False
    return False
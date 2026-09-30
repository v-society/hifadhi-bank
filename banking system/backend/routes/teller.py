#we handle the bank side transactions
#start with bank balance.
#define a function thatUPDATES the bank balance when a deposit is made. The function takes the account number and the amount to be deposited as parameters. It checks if the account number exists in the User.users dictionary, and if it does, it adds the amount to the user's balance and returns True. If the account number does not exist, it returns False. 
from routes import user
from routes.user import User
bank_balance = 0

def update_bank_balance(amount):
    global bank_balance
    bank_balance += amount

    return bank_balance

def withdrawer(amount):
    global bank_balance
    if amount > 0 and amount <= bank_balance:
        bank_balance -= amount
        return True
    else:
        return False
#WORK ON THE WITHDRAWING ENGENE AND ALSO THE BANK POOL


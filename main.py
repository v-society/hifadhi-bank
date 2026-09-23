
from routes.user import User
import getpass
import routes.client, routes.teller
from utils.receipt import deposit_receipt, withdraw_receipt

def print_users():
    print(User.load_users())

print("""
██╗  ██╗██╗███████╗ █████╗ ██████╗ ██╗  ██╗██╗
██║  ██║██║██╔════╝██╔══██╗██╔══██╗██║  ██║██║
███████║██║█████╗  ███████║██║  ██║███████║██║
██╔══██║██║██╔══╝  ██╔══██║██║  ██║██╔══██║██║
██║  ██║██║██║     ██║  ██║██████╔╝██║  ██║██║
╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝

██████╗  █████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
██████╔╝███████║██╔██╗ ██║█████╔╝
██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
██████╔╝██║  ██║██║ ╚████║██║  ██╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

                 SECURE BANKING CLI
                      v1.0.0
""")
print("""=================HIFADH BANK=====================
WELCOME TO HIFADH BANK, YOUR TRUSTED FINANCIAL PARTNER.
We are committed to providing you with secure and reliable banking services.

PLEASE NOTE: This is a simulated banking environment for educational purposes only.
=================HIFADH BANK=====================""")

print("Please select an option:")
print("1. Create Account")
print("2. Login")
print("3. Exit")

# this is the main loop that handles user input and actions
#mainly user creation, login and bank account access. It will keep running until the user chooses to exit.  
while True:
    print("""
╔══════════════════════╗
║       HIFADH         ║
║     BANK CLI         ║
╚══════════════════════╝
""")
    action = input("TELLER: ")

#ACCOUNT CREATION
    if action == "1":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        pin = input("Set your PIN: ")
        new_user = routes.user.User(name, email, set_pin=pin)
        new_user.admin()
        print("Account created successfully!")
        account = routes.user.User.load_users()[-1]
        print("Your account number is:", account["account_number"])
        print("Your card number is:", account["card_number"])

#LOGIN WITH GETPASS ACTIVE AND USER PIN AUTHENTICATION
    elif action == "2":
        card_number = input("Enter your card number: ")
        access = getpass.getpass("Enter your PIN to access your account: ")

        account = routes.user.User.authenticate(card_number, access)
        if account:
            print("Access granted. Welcome back!")

        #TRANSACTION HANDLER
            print("""
            ████████╗███████╗██╗     ██╗     ███████╗██████╗
            ╚══██╔══╝██╔════╝██║     ██║     ██╔════╝██╔══██╗
               ██║   █████╗  ██║     ██║     █████╗  ██████╔╝
               ██║   ██╔══╝  ██║     ██║     ██╔══╝  ██╔══██╗
               ██║   ███████╗███████╗███████╗███████╗██║  ██║
               ╚═╝   ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
            
                             HIFADHI BANK
                          TELLER OPERATIONS
                         ───────────────────
                             SYSTEM v1.0.0""")
            while True:

                print ("Please select a choice:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Logout")

                choice = input("Enter your choice (1, 2, or 3): ")
                if choice == "1":
                    try:
                        amount = float(input("Enter amount to deposit: $"))
                        sec = input('Enter pin to confirm: ')
                        sec = account
                        if routes.client.deposit(account["account_number"], amount):
                            print("Deposit successful!")
                            print("Your new balance is: $", account["balance"])
                            #update bank balance in teller.py
                            routes.teller.update_bank_balance(amount)
                            print(deposit_receipt(account["account_number"], amount))
                        else:
                            print("Deposit failed.")

                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                        break

                elif choice == "2":
                    try:
                        amount = float(input("Enter amount to withdraw: $"))
                        if routes.client.withdraw(account["account_number"], amount):
                            print("Withdrawal successful!")
                            print("Your new balance is: $", account["balance"])
                            #update bank balance in teller.py
                            routes.teller.update_bank_balance(-amount)
                            print(withdraw_receipt(account["account_number"], amount))
                            #print("Bank balance updated. New bank balance is: $", routes.teller.bank_balance)
                        else:
                            print("Withdrawal failed.")

                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                        break


                elif choice == "3":
                    print("Logging out...")
                    break      
    else:
        print('Access Denied')

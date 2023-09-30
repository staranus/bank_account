from bank_account import deposit, withdraw

menu = '''
1. Withdraw
2. Deposit'''

choice = None

choice = int(input("Choose an option: "))
if choice == 1:
    amount_to_withdraw = float(input("Choose amount to withdraw: "))
    deposit(amount_to_withdraw)

elif choice == 2:
    amount_to_deposit = float(input("Choose amount to deposit: "))
    withdraw(amount_to_deposit)
from bank_account import new_bank_account


def user_menu():

    choice = None
    menu = '''
    1. Create new account.
    2. Account login. 
    3. Withdraw money.
    4. Deposit money.
    5. Close account.
    '''

    choice = int(input("Choose an option: "))
    if choice == 1:
        print("New account was created: ")

    elif choice == 2:
        bank_account = int(input("Insert account number: "))
        pin_code = int(input("Insert pin code: "))
        show_balance = new_bank_account.account_login(bank_account, pin_code)

    elif choice == 3:
        amount_to_withdraw = float(input("Enter amount to be withdrawn: "))
        new_bank_account.withdraw(amount_to_withdraw)
    #
    elif choice == 4:
        amount_to_deposit = float(input("Choose amount to deposit: "))
        new_bank_account.deposit(amount_to_deposit)

    elif choice == 5:
        account_number = int(input("Insert account number to close: "))
        new_bank_account.account_closure(account_number)

user_menu()
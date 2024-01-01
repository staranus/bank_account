from bank_account import BankAccount, create_new_account


def user_menu():
    while True:
        print('''
        Welcome to the Bank Account application
        ------------------------
        1. Create a new account.
        2. Account login. 
        ------------------------''')

        try:
            choice = int(input(f"Please choose an option: "))
            if choice == 1:
                account_params = create_new_account()
                new_bank_account = BankAccount(None,*account_params, None, None)
                new_bank_account.create_user_if_doesnt_exist(*account_params)
                break
            elif choice == 2:
                bank_account = int(input("Insert account number: "))
                pin_code = int(input("Insert pin code: "))
                logged_account = BankAccount.account_login(bank_account, pin_code)
                break
                if not logged_account:
                    print("Please try to login later...")
                else:
                    user_actions_inside_account = int(input(f"\n1. Withdraw 2. Deposit. 3. Close account"))
                    if user_actions_inside_account == 1:
                        amount_to_withdraw = float(input("Enter amount to withdraw: "))
                        logged_account.withdraw(amount_to_withdraw)

                    elif user_actions_inside_account == 2:
                        deposit_amount = float(input("Choose amount to deposit: "))
                        logged_account.deposit(deposit_amount)

                    elif user_actions_inside_account == 3:
                        account_number = int(input("Insert account number to close: "))
                        logged_account.account_closure(account_number)
            elif choice != 1 or 2:
                print("Wrong Choice try again")

        except ValueError:
            print("Error")


user_menu()

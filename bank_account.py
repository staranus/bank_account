import typing
from main import db_manager
import random
import datetime


class BankAccount:
    def __init__(self, account_number: int, full_name: str,
                 email: str, address: str, phone_number: str, birth_date,
                 pin_code: int, balance: int):
        self.account_number = account_number
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.pin_code = pin_code
        self.balance = balance

    def to_tuple(self) -> tuple:
        return (self.account_number, self.full_name, self.email, self.address, self.phone_number, self.birth_date,
                self.pin_code)

    @classmethod
    def account_login(cls, account_number, pin_code) -> "BankAccount":
        try:
            query = f"SELECT * FROM bank_account WHERE account_number = ? AND pin_code = ?"
            result = db_manager.execute_query(query, (account_number, pin_code), return_selection=True)
            if result:
                # Unpack the result and exclude the first element (account_number) when creating the instance
                account_instance = cls(*result[0][1:])
                account_instance.account_number = account_number# Create an instance with retrieved data
                print("\n Your current net balance =", account_instance.balance)
                return account_instance
            else:
                print(f"Account not found or pin_code is incorrect")
        except Exception as e:
            print(f"Error in account_login: {type(e).__name__} - {e}")

    def __add_new_user_account_to_db(self) -> typing.Tuple[int, int]:
        pin_code = random.randint(1000, 9999)
        db_manager.execute_query("""INSERT INTO bank_account (
                full_name,email,address,phone_number, birth_date, pin_code) VALUES
                (?,?,?,?,?,?)""", (
            self.full_name, self.email, self.address, self.phone_number, self.birth_date, pin_code))

        # Querying again after inserting the values in order to retrieve the auto-increment number of bank account
        account_number_query = f"SELECT account_number FROM bank_account WHERE email = '{self.email}'"
        account_number = db_manager.execute_query(account_number_query, return_selection=True)[0][0]
        print(f"New account created with account number: {account_number} and pin code: {pin_code} please keep them "
              f"discretely")
        return self.email, pin_code

    # todo - add if account already exists
    def create_user_if_doesnt_exist(self, full_name, email, address, phone_number, birth_date):
        try:
            if all((full_name, email, address, phone_number, birth_date)):
                query = f"SELECT * FROM bank_account WHERE email = ? AND phone_number = ? AND full_name = ?"
                check_if_user_exists = db_manager.execute_query(query, (email, phone_number, full_name),
                                                                return_selection=True)
                if check_if_user_exists:
                    print(f"User already exists")
                else:
                    self.__add_new_user_account_to_db()
            else:
                print("Some parameters are missing")
        except Exception as e:
            print(f"Error: {e}")

    def account_closure(self, account_number):
        try:
            closure_query = "DELETE FROM bank_account WHERE account_number = ?"
            result = db_manager.execute_query(closure_query, self.account_number)
            if result > 0:
                print(f"Bank account '{account_number}' deleted successfully")
            else:
                print(f"No account was found with account number: '{account_number}'. Deletion failed.")
        except Exception as e:
            print(f"Error: {e}")

    def deposit(self, amount_to_deposit):
        self.balance += amount_to_deposit
        deposit_query = "UPDATE bank_account SET balance = ? WHERE account_number = ?"
        # print("SQL Query:", query)
        # print("Parameters:", (self.balance, self.account_number))
        result = db_manager.execute_query(deposit_query, (self.balance, self.account_number))
        if result is not None:
            print("\n Amount deposited: ", amount_to_deposit, "current balance: ", self.balance)
        else:
            print("Deposit failed")

    def withdraw(self, amount_to_withdraw):
        if self.balance >= amount_to_withdraw:
            self.balance -= amount_to_withdraw
            withdraw_query = "UPDATE bank_account SET balance = ? WHERE account_number = ?"
            result = db_manager.execute_query(withdraw_query, (self.balance, self.account_number))
            if result is not None:
                print("\n You Withdrew:", amount_to_withdraw, "current balance: ", self.balance)
            else:
                print("Money withdraw failed")
        else:
            print("\n Insufficient balance")


def create_table() -> None:
    db_manager.execute_query('''CREATE TABLE IF NOT EXISTS bank_account (
                account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                address TEXT,
                phone_number TEXT,
                birth_date TEXT,
                pin_code INT,
                balance INTEGER DEFAULT 0)''', return_selection=True)
    # print(f"Table creation succeeded")


def create_new_account() -> tuple:
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")
    try:
        birth_date = input("Enter birth date (YYYY-MM-DD): ")
        datetime.strptime(birth_date, '%Y-%m-%d')
        return True
    except ValueError:
        print("ValueError")
    return full_name, email, address, phone_number, birth_date


def user_menu():
    print('''
    Welcome to the Bank Account application
    ------------------------
    1. Create a new account.
    2. Account login. 
    ------------------------''')

    choice = int(input(f"Please choose an option: "))
    try:
        if choice == 1:
            account_params = create_new_account()
            new_bank_account = BankAccount(None, *account_params, None, 0)
            new_bank_account.create_user_if_doesnt_exist(*account_params)

        elif choice == 2:
            bank_account = int(input("Insert account number: "))
            pin_code = int(input("Insert pin code: "))
            logged_account = BankAccount.account_login(bank_account, pin_code)
            if not logged_account:
                print("User isn't logged in")
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
    except ValueError:
        print("Error")

user_menu()
create_table()


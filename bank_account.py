import typing
import sqlite3
import traceback
import sys
from main import db_manager
import random


def create_table() -> None:
    db_manager.execute_query('''CREATE TABLE IF NOT EXISTS bank_account (
                account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_identifier TEXT,
                full_name TEXT,
                email TEXT,
                address TEXT,
                phone_number TEXT,
                birth_date TEXT,
                pin_code INT,
                balance INTEGER DEFAULT 0)''', return_selection=True)
    # print(f"Table creation succeeded")


# todo - needs to go before the try-except below, as creation should be before INSERT INTO statement
create_table()


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
        return self.account_number, self.full_name, self.email, self.address, self.phone_number, self.birth_date, self.pin_code

    @staticmethod
    def account_login(account_number, pin_code) -> "BankAccount":
        try:
            query = f"SELECT * FROM bank_account WHERE account_number = {account_number} AND pin_code = {pin_code}"
            # print(query)
            db_manager.execute_query(query, return_selection=True)
            print("\n Net Available Balance =", new_bank_account.balance)
        except ValueError:
            print(f"pin_code or account_number is incorrect")

    def __add_new_user_account_to_db(self) -> typing.Tuple[int, int]:
        pin_code = random.randint(1000, 9999)
        db_manager.execute_query("""INSERT INTO bank_account (
                full_name,email,address,phone_number, birth_date, pin_code) VALUES
                (?,?,?,?,?,?)""", (
            self.full_name, self.email, self.address, self.phone_number, self.birth_date, pin_code))

        # Querying again after inserting the values in order to retrieve the auto-increment nunber of bank account
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
            rows_affected = db_manager.execute_query(f"DELETE FROM bank_account WHERE account_number = {account_number}")
            if rows_affected > 0:
                print(f"Bank account '{account_number}' deleted successfully")
            else:
                print(f"No account found with account number {account_number}. Deletion failed.")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def deposit(self, amount_to_deposit):
        self.balance += amount_to_deposit
        # todo - here, add UPDATE sql statement
        db_manager.execute_query(f"""UPDATE bank_account SET balance = {self.balance} 
                                      WHERE account_number = {self.account_number}""")
        print("\n Amount Deposited: ", amount_to_deposit, "current balance: ", self.balance)

    def withdraw(self, amount_to_withdraw):
        if self.balance >= amount_to_withdraw:
            self.balance -= amount_to_withdraw
            db_manager.execute_query(f"""UPDATE bank_account SET balance = {self.balance} 
                                           WHERE account_number = {self.account_number}""")
            print("\n You Withdrew:", amount_to_withdraw, "current balance: ", self.balance)
        else:
            print("\n Insufficient balance")


def create_a_new_account() -> tuple:
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")
    birth_date = input("Enter birth date (YYYY-MM-DD): ")  # TODO - validation on format
    return full_name, email, address, phone_number, birth_date


account_params = create_a_new_account()
new_bank_account = BankAccount(None, *account_params, None, 0)
new_bank_account.create_user_if_doesnt_exist(*account_params)

# Eventually the pin + account number are being generated by the DB.
# new_bank_account = BankAccount(None, "saar", "gmail@gmail.com", "x", "y", "1990-01-01", None, 10000)
# if new_bank_account is not None:
#     # Account found
#     # print(new_bank_account.to_tuple())
# # else:
# #     print("Account not found.")

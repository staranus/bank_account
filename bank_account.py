from main import db_manager
import sqlite3

# db_manager =

class BankAccount:
    def __init__(self, account_number: int, full_name: str, email: str, address: str, phone_number: str, birth_date,
                 balance: int):
        self.account_number = account_number
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.balance = balance

    def to_tuple(self) -> tuple:
        return self.account_number, self.full_name, self.email, self.address, self.phone_number, self.birth_date, self.balance

    def create_table(self):
        create_table = db_manager.execute_query('''CREATE TABLE IF NOT EXISTS bank_account (
                    account_number INTEGER PRIMARY KEY,
                    full_name TEXT,
                    email TEXT,
                    address TEXT,
                    phone_number TEXT,
                    birth_date TEXT,
                    balance INTEGER)''', return_selection=True)
        print(create_table)


    def deposit(self, amount_to_deposit):
        self.balance += amount_to_deposit
        print("\n Amount Deposited:", amount_to_deposit)

    def withdraw(self, amount_to_withdraw):
        if self.balance >= amount_to_withdraw:
            amount_to_withdraw = int(input("Enter amount to be withdrawn: "))
            self.balance -= amount_to_withdraw
            print("\n You Withdrew:", amount_to_withdraw)
        else:
            print("\n Insufficient balance  ")

    def display_balance(self):
        print("\n Net Available Balance=", self.balance)

def add_user_to_db(bank_account: BankAccount):
    add_user_to_db = db_manager.execute_query("""INSERT INTO bank_account (
            account_number, full_name,email,address,phone_number,
            birth_date, balance) VALUES 
            (?,?,?,?,?)""", bank_account.to_tuple())

new_bank_account = BankAccount("saar", "email", "address", "x", "y", 1990, 1000)
# print(new_bank_account.full_name)
new_bank_account.create_table()
new_bank_account.deposit(100)
new_bank_account.withdraw(5)
new_bank_account.display_balance()

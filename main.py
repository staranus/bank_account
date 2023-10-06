import sqlite3


class DbManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query, params=None, return_selection=False):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if not params:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                if return_selection:
                    return cursor.fetchall()
                else:
                    return cursor.rowcount  # implementation for the account closure
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


db_manager = DbManager("db.db")

if __name__ == '__main__':
    db = DbManager('db.db')
    query = "SELECT * FROM bank_account"
    s = db.execute_query(query, return_selection=True)
    print(s)

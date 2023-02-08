import sqlite3
def create_connection():
     connection = sqlite3.connect("bank.db")
     return connection



def close_connection(connection):
    connection.close()

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                        name TEXT PRIMARY KEY ,
                        balance REAL
                    )""")
    connection.commit()


def create_account(connection, name, balance):
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO accounts (name, balance)
                            VALUES (?,?)""", (name, balance))
        connection.commit()
        return "Account created successfully"
    except sqlite3.IntegrityError:
        return "An account with this name already exists"


def retrieve_account(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("""SELECT name, balance FROM accounts
                      WHERE name = ?""", (account_id,))
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return {"name": result[0], "balance": result[1]}



def deposit(connection, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name=?", (account_id,))
    account = cursor.fetchone()
    if account is None:
        return "Account does not exist"
    else:
        new_balance = account[0] + amount
        cursor.execute("UPDATE accounts SET balance=? WHERE name=?", (new_balance, account_id))
        connection.commit()
        return "Deposit successful"


def withdraw(connection, name, amount):
    cursor = connection.cursor()
    cursor.execute("""SELECT balance FROM accounts
                      WHERE name = ?""", (name,))
    result = cursor.fetchone()
    if result is None:
        return "Account does not exist"
    else:
        balance = result[0]
        if balance < amount:
            return "Insufficient funds"
        else:
            cursor.execute("""UPDATE accounts
                              SET balance = balance - ?
                              WHERE name = ?""", (amount, name))
            connection.commit()
            return balance - amount



connection = create_connection()
create_table(connection)

create_account(connection, "yd1", 100)
deposit(connection, "yd1", 50)
withdraw(connection, "yd", 100)

close_connection(connection)
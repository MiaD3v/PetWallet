from flask import request

class UserDoesNotExistException(Exception):
    pass

class User:
    @staticmethod
    def listUsers():
        ret = [];
        usernames = \
            cursor.execute("SELECT username FROM users;").fetchall()
        for username in usernames:
            ret.append(username[0])
        return ret

    def __init__(self, username):
        cursor = request.sqlite3_cursor
        db_res = \
            cursor.execute( \
                "SELECT username FROM users WHERE username = ? LIMIT 1;",
                [username]).fetchall()
        if len(db_res) < 1:
            raise UserDoesNotExistException(f"The user \"{username}\" does not exist!")
        elif len(db_res) > 1:
            raise UserDoesNotExistException(
                f"There are {len(db_res)} users with the username " +
                "\"{username}\"; this should not be possible.")
        self.username = db_res[0][0];

        # Maybe it is better to use a join here.
        self.budgets = cursor.execute( \
            "SELECT " +
            "budget_id, username, budget_name, low_end, high_end " +
            "FROM budgets " +
            "WHERE username = ?", [self.username]).fetchall()

        self.transactions = \
            cursor.execute(
                "SELECT "                                                      +
                "transaction_id, username, transaction_to,  transaction_name, "+
                "transaction_desc, transaction_amount, transaction_datetime "  +
                "FROM transactions;").fetchall()

    def addBudget(self, budget_name, low_end, high_end):
        cursor = request.sqlite3_cursor
        cursor.execute( \
            "INSERT INTO budgets(username, budget_name, low_end, high_end)"  + \
            "VALUES(?, ?, ?, ?)", \
            [self.username, budget_name, low_end, high_end])
        request.sqlite3_connection.commit()
        self.budgets.append((cursor.lastrowid,
                             self.username,
                             budget_name,
                             low_end,
                             high_end))

    def removeTransaction(self, tid):
        cursor     = request.sqlite3_cursor
        connection = request.sqlite3_connection

        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?;",
                       [tid])
        connection.commit()
        self.transactions = \
            cursor.execute(
                "SELECT "                                                      +
                "transaction_id, username, transaction_to,  transaction_name, "+
                "transaction_desc, transaction_amount, transaction_datetime "  +
                "FROM transactions;").fetchall()

    def addTransaction(self, to, name, desc, amount):
        cursor = request.sqlite3_cursor

        cursor.execute(
            "INSERT INTO " +
            "transactions(username, transaction_to, transaction_name, " +
                         "transaction_desc, transaction_amount, " +
                         "transaction_datetime)" +
            "VALUES(?, ?, ?, ?, ?, DATETIME('now'));",
            [self.username, to, name, desc, amount])

        request.sqlite3_connection.commit()

        self.transactions.append(
            cursor.execute(
                "SELECT transaction_id, username, transaction_to, transaction_name, " +
                "transaction_desc, transaction_amount transaction_datetime FROM " +
                "transactions where transaction_id = ?;",
                [cursor.lastrowid]).fetchall()[0])


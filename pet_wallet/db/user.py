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
                "transaction_id, transactions.username, transaction_to,  transaction_name, "+
                "transaction_desc, transaction_amount, transaction_datetime, " +
                "budget_name " +
                "FROM transactions " +
                "INNER JOIN budgets ON transactions.budget_id = budgets.budget_id " +
                "WHERE transactions.username = ?;", [self.username]).fetchall()
        print(self.transactions)

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
                "transaction_desc, transaction_amount, transaction_datetime, " +
                "budget_name " +
                "FROM transactions " +
                "INNER JOIN budgets ON transactions.budget_id = budgets.budget_id;").fetchall()

    def addTransaction(self, to, name, desc, amount, budget_name):
        cursor = request.sqlite3_cursor

        b_id = \
            cursor.execute("SELECT budget_id FROM budgets WHERE budget_name=?;",
                           [budget_name]).fetchall()[0][0]

        cursor.execute(
            "INSERT INTO " +
            "transactions(username, transaction_to, transaction_name, " +
                         "transaction_desc, transaction_amount, " +
                         "transaction_datetime, budget_id)" +
            "VALUES(?, ?, ?, ?, ?, DATETIME('now'), ?);",
            [self.username, to, name, desc, amount, b_id])

        request.sqlite3_connection.commit()

        self.transactions.append(
            cursor.execute(
                "SELECT transaction_id, username, transaction_to, transaction_name, " +
                "transaction_desc, transaction_amount transaction_datetime FROM " +
                "transactions where transaction_id = ?;",
                [cursor.lastrowid]).fetchall()[0])

    def determineCreatureHappiness(self):
        cursor = request.sqlite3_cursor

        # -1 is < 'low'
        # 0 is between 'low' and 'high'
        # 1 is > 'high'
        budget_statuses = []

        for budget in self.budgets:
            transactions = cursor.execute("SELECT * FROM transactions WHERE budget_id = ?", [budget[0]]).fetchall()
            total = 0
            for tr in transactions:
                total += int(tr[5])
            lo = budget[3]
            hi = budget[4]
            if total < lo:
                budget_statuses.append(-1)
            elif total > hi:
                budget_statuses.append(1)
            else:
                budget_statuses.append(0)

        average = sum(budget_statuses) / len(budget_statuses)

        if average < -0.2:
            return "happy"
        if average > 0.2:
            return "sad"
        return "neutral"




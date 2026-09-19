from . import connection

class UserDoesNotExistException(Exception):
    pass

class User:
    @staticmethod
    def listUsers():
        ret = [];
        usernames = \
            connection.cursor.execute("SELECT username FROM users;").fetchall()
        for username in usernames:
            ret.append(username[0])
        return ret

    def __init__(self, username):
        db_res = \
            connection.cursor.execute( \
                "SELECT username FROM users WHERE username = ? LIMIT 1;",
                [username]).fetchall()
        if len(db_res) < 1:
            raise UserDoesNotExistException(f"The user \"{username}\" does not exist!")
        elif len(db_res) > 1:
            raise UserDoesNotExistException(
                f"There are {len(db_res)} users with the username " +
                "\"{username}\"; this should not be possible.")
        self.username = db_res[0][0];

        # Maybe there is some way to use a JOIN instead, but I think this works
        # better.
        self.budgets = connection.cursor.execute( \
            "SELECT " +
            "budget_id, username, budget_name, low_end, high_end " +
            "FROM budgets " +
            "WHERE username = ?", [self.username]).fetchall()

    def addBudget(self, budget_name, low_end, high_end):
        connection.cursor.execute( \
            "INSERT INTO budgets(username, budget_name, low_end, high_end)"  + \
            "VALUES(?, ?, ?, ?)", \
            [self.username, budget_name, low_end, high_end])
        connection.connection.commit()
        print(connection.cursor.lastrowid)
        self.budgets.append((connection.cursor.lastrowid, self.username, budget_name, low_end, high_end))


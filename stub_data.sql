CREATE TABLE users(
    username TEXT NOT NULL UNIQUE PRIMARY KEY
);

-- TODO: use foreign keys
CREATE TABLE budgets(
    budget_id INTEGER PRIMARY KEY NOT NULL,
    username    TEXT NOT NULL,
    budget_name TEXT NOT NULL,
    low_end INTEGER NOT NULL,
    high_end INTEGER NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username),
    UNIQUE(username, budget_name)
);

INSERT INTO users(username) VALUES('default_user');

INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('default_user', 'Food Budget', 200000, 400000);
INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('default_user', 'Utility Budget', 100000, 150000);

CREATE TABLE transactions(
    transaction_id     INTEGER PRIMARY KEY NOT NULL,
    username              TEXT NOT NULL,
    transaction_to        TEXT NOT NULL,
    transaction_name      TEXT NOT NULL,
    transaction_desc      TEXT NOT NULL,
    transaction_amount INTEGER NOT NULL,
    transaction_datetime  TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
);

INSERT INTO transactions(username,
                         transaction_to,
                         transaction_name,
                         transaction_desc,
                         transaction_amount,
                         transaction_datetime)
    VALUES('default_user',
           'The Store',
           'Groceries',
           'I just bought some grocceries b/c I need to eat.',
           250000,
           DATETIME('now'));


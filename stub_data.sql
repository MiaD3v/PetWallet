CREATE TABLE users (
    username TEXT NOT NULL UNIQUE PRIMARY KEY
);

CREATE TABLE budgets (
    budget_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    budget_name TEXT NOT NULL,
    low_end INTEGER NOT NULL,
    high_end INTEGER NOT NULL,
    UNIQUE(username, budget_name)
);

INSERT INTO users(username) VALUES('test_user');

INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('test_user', 'Food Budget', 200000, 400000);
INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('test_user', 'Utility Budget', 100000, 150000);

INSERT INTO users(username) VALUES('another_user');

INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('another_user', 'Budget #1', 1000, 2000);
INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('another_user', 'Budget #2', 2000, 4000);


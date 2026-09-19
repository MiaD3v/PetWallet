CREATE TABLE users (
    username TEXT NOT NULL UNIQUE PRIMARY KEY
);

-- TODO: use foreign keys
CREATE TABLE budgets (
    budget_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    budget_name TEXT NOT NULL,
    low_end INTEGER NOT NULL,
    high_end INTEGER NOT NULL,
    UNIQUE(username, budget_name)
);

INSERT INTO users(username) VALUES('default_user');

INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('default_user', 'Food Budget', 200000, 400000);
INSERT INTO budgets(username, budget_name, low_end, high_end)
    VALUES('default_user', 'Utility Budget', 100000, 150000);


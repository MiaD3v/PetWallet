from pet_wallet import db

assert db.User.listUsers() == ['test_user', 'another_user']
user = db.User("test_user")
print(user.budgets)
# user.addBudget("Yet Another Test Budget", 500000, 600000)
try:
    user = db.User("hi")
    assert False
except db.UserDoesNotExistException:
    pass


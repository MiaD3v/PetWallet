from flask import render_template
from . import app
from . import db
from .request import Request

@app.route("/settings")
def settings_page():
    with Request() as r:
        user = db.User("default_user")
        budgets = []

        for budget in user.budgets:
            budgets.append((budget[2], centsToString(budget[3]), centsToString(budget[4])))

        return render_template("Settings.html", budgets=budgets)

def centsToString(c):
    return f"{c//100}.{c%100:02}"



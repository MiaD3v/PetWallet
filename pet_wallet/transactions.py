from . import app
from .request import Request
from flask import render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from . import db
from .cents_to_string import centsToString

class AddTransactionForm(FlaskForm):
    transaction_to = \
        StringField("To", \
        validators=[DataRequired(), \
        Length(min=3, max=256, \
        message="You must have at least 3 characters and at most 256 characters in this field!")])
    transaction_name = \
        StringField("Transaction Name", \
        validators=[DataRequired(),     \
        Length(min=3, max=256,          \
        message="You need [3, 256] characters in this field.")])
    transaction_desc = \
        StringField("Transaction Description", \
        validators=[DataRequired(),            \
        Length(min=3, max=1024,                \
        message="You need [3, 1024] characters in this field.")])
    transaction_amount = \
        IntegerField("Transaction Amount (in cents)", \
        validators=[DataRequired(),                   \
        NumberRange(min=0, message="Please enter a positive amount!")])
    submit_field = SubmitField("Submit")

@app.route("/transactions", methods=["GET", "POST"])
def transactions_page():
    with Request() as r:
        form = AddTransactionForm()

        user = db.User('default_user')


        if request.method == "GET":
            transactions = []

            for t in user.transactions:
                transactions.append((t[2], t[3], t[4], "$"+centsToString(t[5]), t[6]))
            return render_template("Transactions.html", form=form, transactions=transactions)
        elif request.method == "POST" and form.validate():
            user.addTransaction(form.transaction_to.data,
                                form.transaction_name.data,
                                form.transaction_desc.data,
                                form.transaction_amount.data)
            return redirect(url_for("transactions_page"))

        return "Bad Request", 400


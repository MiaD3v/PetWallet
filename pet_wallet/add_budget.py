from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from . import app

# TODO: Make my own range field with automatic validation!
class AddBudgetForm(FlaskForm):
    budget_name =                       \
        StringField("Budget Name",      \
                    validators=[        \
                        DataRequired(), \
                        Length(min=3,   \
                               max=256, \
                               message="Budget name must have at least 3 " +
                                       "characters and at most 256 characters!")])
    budget_low =                        \
        IntegerField("Lower Range",     \
            validators=[DataRequired(), \
            NumberRange(min=0, message="Lower range must be positive!")])
    budget_high = \
        IntegerField("Upper Range",     \
            validators=[DataRequired(), \
            NumberRange(min=0, message="Upper range must be positive!")])
    submit_field = SubmitField()

@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    add_budget_form = AddBudgetForm()
    if request.method == "GET":
        return render_template("FORM.html", form=add_budget_form)
    elif request.method == "POST" and  \
        add_budget_form.validate() and \
        add_budget_form.budget_low.data <= add_budget_form.budget_high.data:
        return "Validated form!"
    return "Form did not validate!", 400


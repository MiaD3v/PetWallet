from flask import render_template
from . import app
from .request import Request
from . import db

@app.route("/")
def root():
    with Request() as r:
        user = db.User('default_user')
        return render_template(
            "index.html",
            creature_img="/static/creature_"+user.determineCreatureHappiness()+".PNG")


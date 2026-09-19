from flask import render_template
from . import app
from .request import Request

@app.route("/")
def root():
    with Request() as r:
        return render_template("index.html")


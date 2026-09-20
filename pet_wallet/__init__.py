from flask import Flask, render_template
from . import db
from os import urandom

app = Flask(__name__)

# FIXME: See if /dev/urandom is cryptographically secure or just use OpenSSL.
app.config["SECRET_KEY"] = urandom(32)

from . import root
from . import add_budget
from . import settings
from . import transactions


from flask import Flask, render_template
from . import db

app = Flask(__name__)

from . import root


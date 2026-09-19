from flask import request
from .db.connection import connect

class Request:
    def __init__(self):
        request.sqlite3_connection = connect()
        request.sqlite3_cursor     = request.sqlite3_connection.cursor()

    def __enter__(self):
        pass

    def __exit__(self, exit_type, exit_value, exit_traceback):
        try:     request.sqlite3_cursor.close()
        finally: request.sqlite3_connection.close()


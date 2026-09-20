from . import app
from . import db
from .request import Request

@app.route("/transactions/<tid>", methods=["DELETE"])
def delete_transaction(tid):
    print("hello from delete_transaction")
    with Request() as r:
        try:
            tid = int(tid)
        except ValueError:
            return "invalid transaction id", 404
        user = db.User('default_user')
        user.removeTransaction(tid)


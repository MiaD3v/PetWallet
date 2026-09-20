from . import app
from . import db

# "{{ url_for(delete_transaction) }}"

@app.route("/transactions", methods=["DELETE"])
def delete_transaction(transaction_id):
    with Request() as r:
        try:
            tid = int(transaction_id)
            user.removeTransaction(tid)
        except ValueError:
            return "invalid transaction id", 404
        user = db.User('default_user')


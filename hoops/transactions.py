"""Blueprint for /transaction routes."""

from typing import Any, Dict, List, Optional

from flask import (
    # current_app,
    request,
    jsonify,
    Blueprint,
    Response,
)

from db_wrapper.client import SyncClient

from hoops.core.transactions import (
    create_one,
    read_one,
    read_many,
)
from .response import OkResponse
from .models.transaction import (
    Transaction as Model,
    TransactionData as Data,
)


def create_transactions(database: SyncClient) -> Blueprint:
    """Create Transactions Blueprint."""
    # Setup db model
    model = Model(database)

    # Create Blueprint
    transactions = Blueprint(
        "transactions", __name__, url_prefix="/transaction")

    # Connect to db on Request
    @transactions.before_request
    def connect() -> None:
        database.connect()

    # Disconnect after Request is processed
    @transactions.teardown_request
    def disconnect(_: Any) -> None:
        database.disconnect()

    #
    # Define routes
    #

    @transactions.route("/new", methods=["POST"])
    def new() -> Response:
        """Save given data as new Transaction."""
        body: Optional[Dict[str, Any]] = request.get_json()

        if body is None:
            return jsonify("Request body must not be empty.")

        valid_data, db_method = create_one(body, model)
        result: Data = db_method(valid_data)

        return jsonify(OkResponse(result))

    @transactions.route("/one/<tran_id>", methods=["GET"])
    def one(tran_id: str) -> Response:
        """Get a specific Transaction by a given id."""
        valid_data, db_method = read_one(tran_id, model)
        result: Data = db_method(valid_data)

        return jsonify(OkResponse(result))

    @transactions.route("/many/<limit>", methods=["GET"])
    def many(limit: str) -> Response:
        """Get many Transactions."""
        valid_limit, db_method = read_many(limit, model)
        result: List[Data] = db_method(valid_limit)

        return jsonify(OkResponse(result))

    return transactions

"""Blueprint for /transaction routes."""

from typing import Any, Dict, Optional
from uuid import uuid4

from flask import (
    # current_app,
    request,
    jsonify,
    Blueprint,
    Response,
)

from db_wrapper.client import SyncClient

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

        result: Data = model.create.one(new_transaction)

        return jsonify(OkResponse(result))

    @transactions.route("/one/<tran_id>", methods=["GET"])
    def one(tran_id: str) -> Response:
        """Get a specific Transaction by a given id."""
        result: Data = model.read.one_by_id(tran_id)

        return jsonify(OkResponse(result))

    return transactions

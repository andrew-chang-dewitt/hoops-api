"""Blueprint for /transaction routes."""

from typing import Any, Dict, List, Optional, Tuple

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
from hoops.errors import BadRequest
from hoops.response import OkResponse
from hoops.models.transaction import (
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
    def new() -> Tuple[Response, int]:
        """Save given data as new Transaction."""
        body: Optional[Dict[str, Any]] = request.get_json()

        if body is None:
            raise BadRequest("Request body must not be Null.")

        valid_data, db_method = create_one(body, model)
        result: Data = db_method(valid_data)

        return jsonify(result.dict()), 201

    @transactions.route("/one/<tran_id>", methods=["GET"])
    def one(tran_id: str) -> Response:
        """Get a specific Transaction by a given id."""
        try:
            valid_data, db_method = read_one(tran_id, model)
        except ValueError as err:
            print(str(err))

            if 'badly formed hexadecimal' in str(err):
                raise BadRequest('Invalid transaction id.') from err

            raise err

        result: Data = db_method(valid_data)

        return jsonify(result.dict())

    @transactions.route("/many", methods=["GET"])
    def many() -> Response:
        """Get many Transactions."""
        limit = request.args.get('limit', None)
        page = request.args.get('page', None)
        valid_args, db_method = read_many(limit, page, model)
        result: List[Data] = db_method(*valid_args)

        return jsonify([item.dict() for item in result])

    return transactions

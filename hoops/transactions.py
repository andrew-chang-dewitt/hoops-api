from flask import Blueprint, request, jsonify, Response

transactions = Blueprint(
    "transactions", __name__, url_prefix="/transaction")


@transactions.route("/many", methods=["GET"])
def many() -> Response:
    return jsonify([{
        "name": "a transaction"
    }])

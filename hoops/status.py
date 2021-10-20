from typing import Literal

from flask import Blueprint, request, jsonify, Response

status = Blueprint(
    "status", __name__, url_prefix="/status")


@status.route("/")
def status_route() -> dict[str, Literal[True]]:
    """Check API status at index."""
    return {
        "ok": True,
    }

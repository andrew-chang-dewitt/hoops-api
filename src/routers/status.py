"""Router for `/status`"""

from fastapi.routing import APIRouter
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Status(BaseModel):
    """Status Response."""

    # pylint: disable=too-few-public-methods

    message: str
    ok: bool


# @app.get("/")
async def root() -> Status:
    return Status(
        message="The API is up.",
        ok=True)

status = APIRouter(prefix="/status")
status.add_api_route("/", root, methods=["GET"], response_model=Status)

"""Transaction logic."""

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from uuid import uuid4, UUID

from hoops.models.transaction import (
    Transaction as Model,
    TransactionData as Data,
)


T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

Return = Tuple[T, Callable[[U], V]]


def create_one(
    incoming_data: Dict[str, Any],
    model: Model
) -> Return[Data, Data, Data]:
    """Validate data & return with database method."""
    new_transaction = Data(**{
        **incoming_data,
        "id": uuid4()
    })

    return new_transaction, model.create.one


def read_one(
    requested_id: str,
    model: Model
) -> Return[UUID, UUID, Data]:
    """Validate id as UUID & return with database method."""
    tran_id = UUID(requested_id)

    return tran_id, model.read.one_by_id


def read_many(
    limit: Optional[Union[str, int]],
    page: Optional[Union[str, int]],
    model: Model
) -> Return[Tuple[Optional[int], Optional[int]], Optional[int], List[Data]]:
    """Validate limit as None or int & return with database method."""
    valid_limit = int(limit) if limit else None
    valid_page = int(page) if page else None

    return (valid_limit, valid_page), model.read.many

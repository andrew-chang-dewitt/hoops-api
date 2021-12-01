"""Model utility functions."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple, Union

from db_wrapper.model import sql

from src.models.base import Base


def _build_one_filter(
    column: str,
    value: Any,
    comparator: sql.Composable = sql.SQL("=")
) -> sql.Composed:
    return sql.SQL(
        "AND {column} {comparator} {value}"
    ).format(
        column=sql.Identifier(column),
        comparator=comparator,
        value=sql.Literal(value))


def build_query_equality_filters(filters: Base) -> sql.Composed:
    """Build 'column equals value' filter arguments for query from Model."""
    filter_queries: List[sql.Composed] = []

    for key, value in filters.dict().items():
        if value is not None:
            filter_queries.append(_build_one_filter(key, value))

    return sql.SQL(" ").join(filter_queries)


Condition = Tuple[sql.Composable, Any]
FilterQuery = Union[Condition, sql.Composed]
FilterModel = Dict[str, FilterQuery]


def equals(value: Any) -> Condition:
    """Return equality value pair."""
    return sql.SQL("="), value


def less_than(value: Any) -> Condition:
    """Return less than value pair."""
    return sql.SQL("<"), value


def greater_than(value: Any) -> Condition:
    """Return greater than value pair."""
    return sql.SQL(">"), value


def less_than_or_equal_to(value: Any) -> Condition:
    """Return less than or equal to value pair."""
    return sql.SQL("<="), value


def greater_than_or_equal_to(value: Any) -> Condition:
    """Return greater than or equal to value pair."""
    return sql.SQL(">="), value


def is_not(pair: Condition) -> Condition:
    """Negate a given value pair & return the query."""
    comparator, value = pair
    negated = sql.SQL("NOT {comparator}").format(comparator=comparator)

    return negated, value


def _build_condition(
    column: str,
    value: Any,
    comparator: sql.Composable = sql.SQL("=")
) -> sql.Composed:
    literal_value = sql.Literal(value)

    return sql.SQL(
        "{column} {comparator} {value}"
    ).format(
        column=sql.Identifier(column),
        comparator=comparator,
        value=literal_value)


class LogicalOperator(Enum):
    """Valid SQL logical operators."""

    AND = sql.SQL(" AND ")
    OR = sql.SQL(" OR ")


@dataclass
class Logical:
    """Organize data required to build a logical condition in SQL."""

    operator: LogicalOperator
    conditions: Tuple[Condition, ...]

    def __init__(self, operator: LogicalOperator, *args: Condition) -> None:
        """Create Logical from variable number of arguments as conditions."""
        self.operator = operator
        self.conditions = args


def logical_or(*args: Condition) -> Logical:
    """Combine given conditions with OR operator."""
    return Logical(LogicalOperator.OR, *args)


def logical_and(*args: Condition) -> Logical:
    """Combine given conditions with AND operator."""
    return Logical(LogicalOperator.AND, *args)


def _build_logical(
    log_operator: LogicalOperator,
    *args: sql.Composable,
) -> sql.Composable:
    """Compose a Logical into SQL."""
    return log_operator.value.join(list(args))


def build_query_filters(filters: FilterModel) -> sql.Composed:
    """Build complex filters from modified Model."""
    filter_queries: List[sql.Composed] = []

    for key, value in filters.items():
        if isinstance(value, Logical):
            query_filter = _build_logical(
                value.operator,
                *[_build_condition(key, condition, comparator)
                    for comparator, condition in value.conditions])
            filter_queries.append(query_filter)

        elif value is not None:
            comparator, condition = value

            if condition is not None:
                query_filter = _build_condition(key, condition, comparator)
                filter_queries.append(query_filter)

    if filter_queries:
        composed_filter_queries = sql.SQL(" AND ").join(filter_queries)

        return sql.SQL(
            " AND {composed}"
        ).format(
            composed=composed_filter_queries)

    return sql.SQL("")


def build_pagination_filters(
    limit: int,
    page: int,
    sort: str,
) -> sql.Composed:
    """Construct SQL filters for adding pagination to a query."""
    # offset is n times limit
    # if limit = 50: (0, 0), (1, 50), ... (n+1, 50*n)
    offset = page * limit

    return sql.SQL(
        " ORDER BY {sort} DESC LIMIT {limit} OFFSET {offset} "
    ).format(
        sort=sql.Identifier(sort),
        limit=sql.Literal(limit),
        offset=sql.Literal(offset))

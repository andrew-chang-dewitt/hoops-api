from typing import Callable, Optional, TypeVar, Union

from src.models.filters import Condition, Logical

Value = TypeVar('Value')
FilterFn = Callable[..., Condition]


def a_b_both_or_none(
    value_a: Optional[Value],
    value_b: Optional[Value],
    fn_a: FilterFn,
    fn_b: FilterFn,
    both_fn: Callable[..., Logical],
) -> Union[Condition, Logical, None]:
    """Determine filter query depending on given Values A & B."""
    # short circuit to None if both are None
    if value_a is None and value_b is None:
        return None

    # else parse as both function if both are present
    if value_a is not None and value_b is not None:
        return both_fn(fn_a(value_a), fn_b(value_b))

    # and single condition if only one is present
    if value_a is not None and value_b is None:
        return fn_a(value_a)

    if value_a is None and value_b is not None:
        return fn_b(value_b)

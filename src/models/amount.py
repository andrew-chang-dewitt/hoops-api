from pydantic import ConstrainedDecimal  # pylint: disable=E0611


class Amount(ConstrainedDecimal):
    """A Decimal, constrained to 2 decimal places."""

    # pylint: disable=too-few-public-methods

    decimal_places = 2

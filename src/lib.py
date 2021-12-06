"""Application logic."""

from typing import Optional, Tuple, Union

from src.models.amount import Amount
from src.models import Balance, EnvelopeOut

FundsHolder = Union[Balance, EnvelopeOut]


def _get_balance(item: FundsHolder) -> Amount:
    """Get the balance of a given FundsHolder."""
    return item.amount if isinstance(item, Balance) else item.total_funds


class NotEnough(Exception):

    def __init__(self, funds: Amount, source: Amount) -> None:
        super().__init__(f"Not enough funds in {source} to remove {funds}.")


def _remove_funds(funds: Amount, source: Amount) -> Amount:
    """Safely subtract Funds from Source."""
    # subtract funds from source
    new_amount = source - funds

    # check enough
    if new_amount < 0:
        # if no, raise NotEnough
        raise NotEnough(funds=funds, source=source)

    # else, return new source balance
    return Amount(new_amount)


def _add_funds(funds: Amount, target: Amount) -> Amount:
    """Add funds to target."""
    return Amount(funds + target)


def _build_funds_holder(
    balance: Amount,
    original_item: FundsHolder,
) -> Optional[EnvelopeOut]:
    """Create Envelope if Envelope, else None."""
    if isinstance(original_item, EnvelopeOut):
        return EnvelopeOut(**{
            **original_item.dict(),
            "total_funds": balance
        })

    return None


def move_funds(
    amount: Amount,
    src: FundsHolder,
    target: FundsHolder
) -> Tuple[Optional[EnvelopeOut], Optional[EnvelopeOut]]:
    """Move amount of funds from source to target & return new objects."""
    # get balances of src & target
    src_bal = _get_balance(src)
    target_bal = _get_balance(target)

    # calculate new balances
    new_src_bal = _remove_funds(amount, src_bal)
    new_target_bal = _add_funds(amount, target_bal)

    # create result target & result src
    # if Envelope, create new envelope w/ updated total_funds
    # else assign None
    result_src = _build_funds_holder(
        balance=new_src_bal,
        original_item=src)
    result_target = _build_funds_holder(
        balance=new_target_bal,
        original_item=target)

    return result_src, result_target

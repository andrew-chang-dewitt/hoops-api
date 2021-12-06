from unittest import main, TestCase

from tests.factories.models import Balance, EnvelopeOut

from src.models.amount import Amount
from src.lib import move_funds


class TestMoveFunds(TestCase):
    """Move funds."""

    def test_move_funds_available_to_envelope(self) -> None:
        """Returns new Envelope."""
        env = EnvelopeOut.create(total_funds=0)
        bal = Balance.create(amount=5)

        _, new_env = move_funds(
            amount=Amount(3),
            src=bal,
            target=env)

        self.assertEqual(new_env.total_funds, 3)

    def test_move_funds_envelope_to_available(self) -> None:
        """Returns new Envelope."""
        env = EnvelopeOut.create(total_funds=5)
        bal = Balance.create(amount=0)

        new_env, _ = move_funds(
            amount=Amount(3),
            src=env,
            target=bal)

        self.assertEqual(new_env.total_funds, 2)

    def test_move_funds_envelope_to_envelope(self) -> None:
        """Returns new Envelopes"""
        src = EnvelopeOut.create(total_funds=5)
        tgt = EnvelopeOut.create(total_funds=0)

        new_source, new_target = move_funds(
            amount=Amount(3),
            src=src,
            target=tgt)

        with self.subTest():
            self.assertEqual(new_source.total_funds, 2)
        with self.subTest():
            self.assertEqual(new_target.total_funds, 3)


if __name__ == '__main__':
    main()

"""Backend constants."""

from enum import Enum
from decimal import Decimal


class TransactionType(str, Enum):
    """Valid transaction types."""

    INCOME = "income"
    EXPENSE = "expense"


# Maximum allowed account balance
MAX_BALANCE = Decimal("99999999.99")

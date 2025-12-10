from enum import Enum
from decimal import Decimal

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

MAX_BALANCE = Decimal("99999999.99")
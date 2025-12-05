"""Database services for finance accounts."""

from .... import db
from ...models.models import Transaction, Account
from ..users.users_services import get_user
from .constants import TransactionType


# returns account (success) or None (failed)
# private use
def _get_account_balance(email):
    account = get_user(email).account
    if account:
        return account
    else:
        raise Exception("Account not found")


# returns True (success) or None (failed)
# public use
def create_account(email):
    account = Account(user_email=email, balance=0.00)
    try:
        db.add(account)
        db.commit()
        return {"success": True, "message": "Added account succesfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error creating account: {str(e)}"}


# returns account (success) or None (failed)
# public use
def get_account(email):
    try:
        account = _get_account_balance(email)
        if account:
            return {
                "success": True,
                "message": "Retrieved account succesfully",
                "account": account,
            }
        else:
            return {"success": False, "error": "Account not found"}
    except Exception as e:
        return {"success": False, "error": f"Error retreiving account: {str(e)}"}


# returns account balance (success) or None (failed)
# public use
def get_account_balance(email):
    try:
        account = _get_account_balance(email)
        if account:
            return {
                "success": True,
                "message": "Retrieved account balance succesfully",
                "balance": account.balance,
            }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error retreiving balance: {str(e)}"}


# returns account transactions (success) or None (failed)
# public use
def get_account_transactions(email):
    try:
        account = _get_account_balance(email)
        if account:
            return {
                "success": True,
                "message": "Retrieved account transaction history succesfully",
                "transactions": account.transactions,
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retreiving account transactions: {str(e)}",
        }


# returns True (success) or None (failed)
# public use
def add_income(email, amount, description="None"):
    try:
        account = _get_account_balance(email)
        starting_balance = account.balance
        ending_balance = account.balance + amount
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.INCOME,
            description=description,
            starting_balance=starting_balance,
            ending_balance=ending_balance,
        )

        db.add(transaction)
        account.balance += amount
        db.commit()
        return {
            "success": True,
            "message": "Retrieved income succesfully",
            "updatedBalance": account.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error adding income: {str(e)}"}


# returns True (success) or None (failed)
# there is a possible information leak here in the Exception
def add_expense(email, amount, description="None"):
    try:
        account = _get_account_balance(email)
        starting_balance = account.balance
        ending_balance = account.balance - amount
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            description=description,
            starting_balance=starting_balance,
            ending_balance=ending_balance,
        )

        db.add(transaction)
        account.balance -= amount
        db.commit()
        return {
            "success": True,
            "message": "Retrieved expense succesfully",
            "updatedBalance": account.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error adding expense: {str(e)}"}

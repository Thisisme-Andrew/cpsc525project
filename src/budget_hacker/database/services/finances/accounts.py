"""Database services for finance accounts."""

from decimal import Decimal
from .budgets import _get_total_budgeted_funds
from .constants import TransactionType, MAX_BALANCE
from ..users.users import _get_user
from ...models.models import Transaction, Account
from .... import db


def _create_account(user_email: str):
    """Create a finance account for the user.

    :param user_email: User email.
    :type user_email: str
    """
    try:
        account = Account(user_email=user_email, balance=0.00)
        db.add(account)
        db.commit()
    except Exception:
        db.rollback()
        raise


def _get_account(user_email: str) -> Account:
    """Gets a user's financial account.

    :param user_email: User email.
    :type user_email: str
    :return: The user's account.
    :rtype: Account
    """
    return _get_user(user_email).account


def get_account(user_email: str) -> dict:
    """Request to get a user's account.

    :param user_email: User email.
    :type user_email: str
    :return: Reqponse object.
    :rtype: dict
    """
    try:
        account = _get_account(user_email)
        return {
            "success": True,
            "message": "Account retrieved succesfully.",
            "account": account,
        }
    except Exception as e:
        return {"success": False, "error": f"Error retreiving account: {str(e)}"}


def get_account_balance(user_email: str) -> dict:
    """Request to get a user's account balance.

    :param user_email: User email
    :type user_email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        account = _get_account(user_email)
        return {
            "success": True,
            "message": "Account balance retrieved succesfully.",
            "balance": account.balance,
        }
    except Exception as e:
        return {"success": False, "error": f"Error retreiving balance: {str(e)}"}


def _get_available_account_funds(user_email: str) -> Decimal:
    """Gets a user's available account funds (i.e., funds that have not been allocated to a budget).

    :param user_email: User email.
    :type user_email: str
    :return: The user's available account funds.
    :rtype: Decimal"""
    account_balance = _get_account(user_email).balance
    total_budgeted_funds = _get_total_budgeted_funds(user_email)
    return account_balance - total_budgeted_funds


def get_available_account_funds(user_email: str) -> dict:
    """Request to get a user's available account funds (i.e., funds that have not been allocated
    to a budget).

    :param user_email: User email.
    :type user_email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        available_account_funds = _get_available_account_funds(user_email)
        return {
            "success": True,
            "message": "Available account funds retrieved succesfully.",
            "availableFunds": available_account_funds,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving available account funds: {str(e)}",
        }


def get_transactions(user_email: str) -> dict:
    """Request to get a user's transactions.

    :param user_email: User email.
    :type user_email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        transactions = _get_account(user_email).transactions
        return {
            "success": True,
            "message": "Account transaction history retrieved succesfully.",
            "transactions": transactions,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retreiving account transactions: {str(e)}",
        }


def _add_income(
    user_email: str, amount: Decimal, description: str = "None", commit: bool = True
):
    """Adds an income amount to a user's account.

    :param user_email: User email.
    :type user_email: str
    :param amount: Income amount.
    :type amount: Decimal
    :param description: Income description for transaction history, defaults to "None"
    :type description: str, optional
    :param commit: Flag to automatically commit the change, defaults to True
    :type commit: bool, optional
    """
    try:
        # Validate the amount
        if amount < 0:
            raise RuntimeError("Amount must be positive.")

        # Get the user's account
        account = _get_account(user_email)

        # Add the amount to the user's account balance
        starting_balance = account.balance
        ending_balance = account.balance + amount
        if ending_balance > MAX_BALANCE:
            raise RuntimeError(
                f"Amount ${amount} plus current balance ${starting_balance} exceeds the maximum allowed account balance of ${MAX_BALANCE}."
            )
        account.balance += amount

        # Record the transaction
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.INCOME,
            description=description,
            starting_balance=starting_balance,
            ending_balance=ending_balance,
        )
        db.add(transaction)

        if commit:
            db.commit()
    except Exception:
        db.rollback()
        raise


def add_income(user_email: str, amount: Decimal, description: str = "None") -> dict:
    """Request to add an income amount to a user's account.

    :param user_email: User email.
    :type user_email: str
    :param amount: Income amount.
    :type amount: Decimal
    :param description: Income description for transaction history, defaults to "None"
    :type description: str, optional
    :return: Response object.
    :rtype: dict
    """
    try:
        _add_income(user_email, amount, description)
        return {
            "success": True,
            "message": "Income retrieved succesfully.",
            "updatedBalance": _get_account(user_email).balance,
        }
    except Exception as e:
        return {"success": False, "error": f"Error adding income: {str(e)}"}


def _add_expense(
    user_email: str, amount: Decimal, description: str = "None", commit: bool = True
):
    """Adds an expense amount to a user's account.

    :param user_email: User email.
    :type user_email: str
    :param amount: Expense amount.
    :type amount: Decimal
    :param description: Expense description for transaction history, defaults to "None"
    :type description: str, optional
    :param commit: Flag to automatically commit the change, defaults to True
    :type commit: bool, optional
    """
    try:
        # Validate the amount
        if amount < 0:
            raise RuntimeError("Amount must be positive.")

        # Get the user's account and available funds
        account = _get_account(user_email)
        starting_available_funds = _get_available_account_funds(user_email)

        # Subtract the amount from the available funds
        ending_available_funds = starting_available_funds - amount
        if ending_available_funds < 0:
            raise RuntimeError(f"Insufficient available funds.")
        account.balance -= amount

        # Record the transaction
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            description=description,
            starting_balance=starting_available_funds,
            ending_balance=ending_available_funds,
        )
        db.add(transaction)

        if commit:
            db.commit()
    except Exception:
        db.rollback()
        raise


def add_expense(user_email: str, amount: Decimal, description: str = "None") -> dict:
    """Request to add an expense amount to a user's account.

    :param user_email: User email.
    :type user_email: str
    :param amount: Espense amount.
    :type amount: Decimal
    :param description: Expense description for transaction history, defaults to "None"
    :type description: str, optional
    :return: Response object.
    :rtype: dict
    """
    try:
        _add_expense(user_email, amount, description)
        return {
            "success": True,
            "message": "Expense retrieved succesfully.",
            "updatedBalance": _get_account(user_email).balance,
        }
    except Exception as e:
        return {"success": False, "error": f"Error adding expense: {str(e)}"}


def _send_money(
    sender_email: str, receiver_email: str, amount: Decimal, description: str = "None"
) -> dict:
    """Sends money to another user's account.

    :param sender_email: Sender email.
    :type sender_email: str
    :param receiver_email: Receiver email.
    :type receiver_email: str
    :param amount: Amount to send.
    :type amount: Decimal
    :param description: Description for transaction histories, defaults to "None"
    :type description: str, optional
    :return: Response object
    :rtype: dict
    """
    try:
        # Add the expense to the sender
        _add_expense(sender_email, amount, description, commit=False)
        # Add the income to the receiver
        _add_income(receiver_email, amount, description, commit=False)
        # Commit the changes
        db.commit()
    except Exception:
        db.rollback()
        raise


def send_money(
    sender_email: str, receiver_email: str, amount: Decimal, description: str = "None"
) -> dict:
    """Request to send money to another user's account.

    :param sender_email: Sender email.
    :type sender_email: str
    :param receiver_email: Receiver email.
    :type receiver_email: str
    :param amount: Amount to send.
    :type amount: Decimal
    :param description: Description for transaction histories, defaults to "None"
    :type description: str, optional
    :return: Response object
    :rtype: dict
    """
    description = f"({amount} from {sender_email} to {receiver_email}): " + description
    try:
        _send_money(sender_email, receiver_email, amount, description)
        return {"success": True, "message": "Money sent succesfully."}
    except Exception as e:
        return {"success": False, "error": f"Error sending money: {str(e)}"}

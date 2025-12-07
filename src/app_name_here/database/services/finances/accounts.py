"""Database services for finance accounts."""

from .... import db
from ...models.models import Transaction, Account
from ..users.users_services import get_user
from .constants import TransactionType, MAX_BALANCE


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
        return {"success": True, "message": "Account created succesfully."}
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
                "message": "Account retrieved succesfully.",
                "account": account,
            }
        else:
            return {"success": False, "error": "Account not found."}
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
                "message": "Account balance retrieved succesfully.",
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
                "message": "Account transaction history retrieved succesfully.",
                "transactions": account.transactions,
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retreiving account transactions: {str(e)}",
        }

# private use
def _add_income(email, amount, description="None"):
    try:
        if amount < 0:
            raise Exception("Amount cannot be negative")
        
        account = _get_account_balance(email)
        starting_balance = account.balance
        if starting_balance + amount > MAX_BALANCE:
            raise Exception(f"Amount ({amount} plus current balance ({starting_balance}) is greater than account capacity)")
        
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
    except Exception:
        raise


# returns True (success) or None (failed)
# public use
def add_income(email, amount, description="None"):
    try:
        if amount < 0:
            raise Exception("Amount cannot be negative")
        
        account = _get_account_balance(email)
        starting_balance = account.balance
        if starting_balance + amount > MAX_BALANCE:
            raise Exception(f"Amount ({amount} plus current balance ({starting_balance}) is greater than account capacity)")
        
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
            "message": "Income retrieved succesfully.",
            "updatedBalance": account.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error adding income: {str(e)}"}      


# private use
def _add_expense(email, amount, description="None"):
    try:
        if amount < 0:
            raise Exception("Amount cannot be negative, enter expense as a positive number")
        
        account = _get_account_balance(email)
        starting_balance = account.balance
        if starting_balance - amount < 0:
            raise Exception(f"Insufficient funds")
        
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
    except Exception:
        raise

# returns True (success) or None (failed)
def add_expense(email, amount, description="None"):
    try:
        if amount < 0:
            raise Exception("Amount cannot be negative, enter expense as a positive number")
        
        account = _get_account_balance(email)
        starting_balance = account.balance
        if starting_balance - amount < 0:
            raise Exception(f"Insufficient funds")
        
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
            "message": "Expense retrieved succesfully.",
            "updatedBalance": account.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error adding expense: {str(e)}"}

def send_money(sender_email, receiver_email, amount, description="None"):
    description = f"({amount} from {sender_email} to {receiver_email}): " + description
    try:
        account = _get_account_balance(sender_email)
        if account.balance < amount:
            raise Exception("Insufficient funds")
        
        _add_income(receiver_email, amount, description)
        
        _add_expense(sender_email, amount, description)
        
        db.commit()

        return {
            "success": True,
            "message": "Money sent succesfully."
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error sending money: {str(e)}"}
    

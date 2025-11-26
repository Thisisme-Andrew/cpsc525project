from .... import db
from ...models.models import User, Transaction, Account
from ..users.users_services import get_user
from .constants import TransactionType

# returns account (success) or None (failed)
# private use
def get_account_private(email):
    account = get_user(email).account
    if account:
        return account
    else:
        raise Exception("Account not found")

# returns True (success) or None (failed)
# public use
def add_account(email):
    account = Account(user_email=email, balance=0.00)
    try:
        db.add(account)
        db.commit()
        print("Created account successfully!")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error creating account: {str(e)}")
        return None
    
# returns account (success) or None (failed)
# public use
def get_account(email):
    try:
        account = get_user(email).account
        if account:
            return account
        else:
            raise Exception("Account not found")
    except Exception as e:
        print(f"Error retreiving account: {str(e)}")
        return None

# returns account balance (success) or None (failed)
# public use
def get_balance(email):
    try:
        account = get_account_private(email)
        if account:
            return account.balance
    except Exception as e:
        db.rollback()
        print(f"Error retreiving balance: {str(e)}")
        return None
    
# returns account transactions (success) or None (failed)
# public use
def get_account_transactions(email):
    try:
        account = get_account_private(email)
        if account:
            return account.transactions
    except Exception as e:
        print(f"Error retreiving account transactions: {str(e)}")
        return None

# returns True (success) or None (failed)
# public use
def add_income(email, amount, description="None"):
    try:
        account = get_account_private(email)
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.INCOME,
            description=description
        )

        db.add(transaction)
        account.balance += amount
        db.commit()
        print("Added Income successfully!")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding income: {str(e)}")
        return False

# returns True (success) or None (failed)
# there is a possible information leak here in the Exception
def add_expense(email, amount, description="None"):
    try:
        account = get_account_private(email)
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=TransactionType.EXPENSE,
            description=description
        )
        
        db.add(transaction)
        account.balance -= amount
        db.commit()
        print("Added expense successfully!")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding expense: {str(e)}")
        return False
    

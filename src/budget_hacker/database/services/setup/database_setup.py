"""Initial setup to populate the database with default data."""

from decimal import Decimal

from ..finances.budgets import create_budget
from .... import engine
from ...models.models import Base
from ..users.users import create_user
from ..finances.accounts import add_income

# List of default users to create (<username>, <passwored>)
DEFAULT_USERS = [("alice@gmail.com", "password"), ("bob@gmail.com", "password")]


def run_db_setup():
    """
    Resets and repopulates the database with default data.
    """
    # Drop and recreate all tables.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Populate the default users.
    for email, password in DEFAULT_USERS:
        create_user(email, password)
        create_budget(email, "New Car", Decimal(10000))

    # Add a default income to Alice's account
    add_income("alice@gmail.com", 12345, "Grandma's inheritance")

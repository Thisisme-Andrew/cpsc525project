"""
Initial setup to populate the database with default data.
"""

from decimal import Decimal

from ..finances.budgets import create_budget
from .... import db, engine
from ...models.models import Base, User
from ..users.users_services import create_user

DEFAULT_USERS = [
    User(
        email="alice@gmail.com",
        # Password: "password"
        password="8a264d3fec7cbc4a2650d416a4485875759ab8282011719525cb95d3d88c18fb",
    ),
    User(
        email="bob@gmail.com",
        # Password: "password"
        password="8a264d3fec7cbc4a2650d416a4485875759ab8282011719525cb95d3d88c18fb",
    ),
]


def run_db_setup():
    """
    Resets and repopulates the database with default data.
    """
    # Drop and recreate all tables.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Populate default users.
    for user in DEFAULT_USERS:
        create_user(user.email, user.password)
        create_budget(user.email, "Car", Decimal(10000))

    # Commit all changes to the database.
    db.commit()

"""
Initial setup to populate the database with default data.
"""

from .... import db, engine
from ...models.models import Base, User

DEFAULT_USERS = [
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
        db.add(user)

    # Commit all changes to the database.
    db.commit()

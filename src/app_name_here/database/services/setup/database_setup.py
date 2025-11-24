"""
Initial setup to populate the database with default data.
"""

from .... import db, engine
from ...models.models import Base, User, FooBar

DEFAULT_USERS = [
    User(email="jdoe@gmail.com", password="password123!"),
    User(email="dsmith@gmail.com", password="abcdefg123!"),
]

DEFAULT_FOOBARS = [
    FooBar(foo=123, bar="I am the first bar example"),
    FooBar(foo=20, bar="I am the second bar example"),
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
    
    # Populate default foobars
    for foobar in DEFAULT_FOOBARS:
        db.add(foobar)

    # Commit all changes to the database.
    db.commit()

"""
Application runner.
"""

from . import db
from .database_setup import run_db_setup
from .models import User, FooBar


def run():
    run_db_setup()

    # Dummy data example
    print("Users:")
    for user in db.query(User).all():
        print(f"\tUser({user.email}, {user.password})")
    
    print()

    print("FooBars:")
    for foobar in db.query(FooBar).all():
        print(f"\tFooBar({foobar.foo}, {foobar.bar})")
    
    # Main application loop
    while True:
        # Dummy CLI interaction example
        user_input = input("Sample app input: ")
        print(f"Your input was: {user_input}")

        if user_input == 'hack':
            print("You hacked the program!")
            break

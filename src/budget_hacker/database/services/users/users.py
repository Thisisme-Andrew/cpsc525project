"""Database services for users."""

import hashlib

from ...models.models import User
from .... import db

# Password salt
SALT = "CPSC525SecurePasswordSalt123!"


def _get_user(user_email: str) -> User:
    """Gets the User entry for a given user's email.

    :param user_email: User email.
    :type user_email: str
    :return: User entry.
    :rtype: User
    """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise RuntimeError("User not found.")
    return user


def login(user_email: str, password: str) -> dict:
    """Request to log into a user's account.

    :param user_email: User email.
    :type user_email: str
    :param password: User password.
    :type password: str
    :return: Response object.
    :rtype: dict
    """
    try:
        # Find the User object for the provided email
        user = db.query(User).filter(User.email == user_email).first()
        hashed_pw = hashlib.sha256((password + SALT).encode()).hexdigest()
        if not user or hashed_pw != user.password:
            return {"success": False, "error": "Incorrect username or password."}
        return {"success": True, "message": "Login successful."}
    except Exception as e:
        return {"success": False, "error": f"Error logging in: {str(e)}"}


def _create_user(user_email: str, password: str):
    """Creates a user account.

    :param user_email: User email.
    :type user_email: str
    :param password: User password
    :type password: str
    """
    try:
        # Deferred imports to avoid circular dependencies
        from ..finances.accounts import _create_account

        # Hash the password
        hashed_pw = hashlib.sha256((password + SALT).encode()).hexdigest()

        # Create and add the user to the database
        user = User(email=user_email, password=hashed_pw)
        db.add(user)

        # Create a finance account for the user
        _create_account(user_email)
    except Exception:
        db.rollback()
        raise


def create_user(user_email: str, password: str) -> dict:
    """Request to create a user account.

    :param user_email: User email.
    :type user_email: str
    :param password: User password.
    :type password: str
    :return: Response object.
    :rtype: dict
    """
    try:
        _create_user(user_email, password)
        return {"success": True, "message": f"User created successfully: {user_email}."}
    except Exception as e:
        return {"success": False, "error": f"Error creating user: {str(e)}"}


def _change_password(user_email: str, old_password: str, new_password: str):
    """Change a user's password.

    :param user_email: User email.
    :type user_email: str
    :param old_password: Old password.
    :type old_password: str
    :param new_password: New password.
    :type new_password: str
    """
    try:
        if old_password == new_password:
            raise RuntimeError("New password must be different than the old password.")

        # get the user in the db
        user = _get_user(user_email)

        # Hash the passwords
        old_hashed_pw = hashlib.sha256((old_password + SALT).encode()).hexdigest()
        new_hashed_pw = hashlib.sha256((new_password + SALT).encode()).hexdigest()

        # Confirm the old password matches
        if user.password != old_hashed_pw:
            return {"success": False, "error": "Old password does not match."}

        # Change to the new password
        user.password = new_hashed_pw
        db.commit()
    except Exception:
        db.rollback()
        raise


def change_password(user_email: str, old_password: str, new_password: str) -> dict:
    """Request to change a user's password.

    :param user_email: User email.
    :type user_email: str
    :param old_password: Old password.
    :type old_password: str
    :param new_password: New password.
    :type new_password: str
    :return: Response object.
    :rtype: dict
    """
    try:
        _change_password(user_email, old_password, new_password)
        return {
            "success": True,
            "message": f"Password changed successfully for user: {user_email}.",
        }

    except Exception as e:
        return {"success": False, "error": f"Error changing password: {str(e)}"}


def _remove_user(user_email: str):
    """Remove a user.

    :param user_email: User email.
    :type user_email: str
    """
    try:
        # Get the user
        user = _get_user(user_email)
        db.delete(user)
        db.commit()
    except Exception:
        db.rollback()
        raise


def remove_user(user_email: str) -> dict:
    """Request to remove a user.

    :param user_email: User email.
    :type user_email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        _remove_user(user_email)
        return {
            "success": True,
            "message": f"User removed successfully: {user_email}.",
        }

    except Exception as e:
        return {"success": False, "error": f"Error removing user: {str(e)}"}

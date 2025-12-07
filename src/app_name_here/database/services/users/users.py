from .... import db
from ...models.models import User


# returns the user or raises exception (failed)
# private use
def get_user(email):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    else:
        raise Exception("User not found")


# returns True (success) or False (failed)
# public use
def login(email, password):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or password != user.password:
            return {"success": False, "error": "Incorrect username or password."}
        return {"success": True, "message": "Login successful."}
    except Exception as e:
        return {"success": False, "error": f"Error logging in: {str(e)}"}


# returns True (success) or False (failed)
# public use
def create_user(email, password):
    # Deferred imports to avoid circular dependencies
    from ..finances.accounts import _create_account

    user = User(email=email, password=password)
    try:
        db.add(user)
        _create_account(email)
        db.commit()
        return {"success": True, "message": f"User created successfully: {email}."}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error creating user: {str(e)}"}


# there is a possible information leak here in the Exception
# returns True (success) or False (failed)
# public use
def change_password(email, old_password, new_password):
    try:
        # get the user in the db
        user = get_user(email)

        # Confirm the old password matches
        if user.password != old_password:
            return {"success": False, "error": "Old password does not match."}

        # Change to the new password
        user.password = new_password
        db.commit()
        return {
            "success": True,
            "message": f"Password changed successfully for user: {email}.",
        }

    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error changing password: {str(e)}"}


# returns True (success) or False (failed)
# public use
def remove_user(email):
    try:
        # get the user in the db
        user = get_user(email)

        if user:
            db.delete(user)
            db.commit()
            return {"success": True, "message": f"User removed successfully: {email}."}

    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error removing user: {str(e)}"}

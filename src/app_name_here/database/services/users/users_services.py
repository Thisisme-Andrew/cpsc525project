from .... import db
from ...models.models import User

def get_user(email):
    try:
        user = db.query(User).filter(User.email == email).first() 
        if user:
            return user
        else:
            raise Exception("User not found")
    except Exception as e:
        db.rollback()
        print(f"Error retreiving user password: {str(e)}")
        return None


def add_user(email, password):
    user = User(email=email, password=password)
    try:
        db.add(user)
        db.commit()
        print("Created user successfully!")
        return user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
        return None

def change_password(email, password):
    try:
        # get the user in the db
        user = get_user(email)

        if user:
            user.password = password
            db.commit()
            return user
    
    except Exception as e:
        db.rollback()
        print(f"Error changing password: {str(e)}")
        return None
      

def remove_user(email):
    try:
        # get the user in the db
        user = get_user(email)

        if user:
            db.delete(user)
            db.commit()
            return True
        else: 
            return False
    
    except Exception as e:
        db.rollback()
        print(f"Error removing user: {str(e)}")
        return False
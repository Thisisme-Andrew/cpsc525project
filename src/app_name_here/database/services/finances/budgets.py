from decimal import Decimal
from .... import db
from ...models.models import Budget


def create_budget(user_email: str, name: str, goal: Decimal):
    budget = Budget(user_email=user_email, name=name, goal=goal, balance=Decimal(0))
    try:
        db.add(budget)
        db.commit()
        return {"success": True, "message": "Added budget succesfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error creating budget: {str(e)}"}

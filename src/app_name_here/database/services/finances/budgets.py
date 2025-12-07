"""Database services for budgets."""

from decimal import Decimal
from ..users.users import get_user
from ...models.models import Budget
from .... import db


def create_budget(user_email: str, name: str, goal: Decimal) -> dict:
    """Request to create and add a budget to the database.

    :param user_email: User email.
    :type user_email: str
    :param name: Budget name.
    :type name: str
    :param goal: Budget goal.
    :type goal: Decimal
    :return: Response object.
    :rtype: dict
    """
    budget = Budget(user_email=user_email, name=name, goal=goal, balance=Decimal(0))
    try:
        db.add(budget)
        db.commit()
        return {"success": True, "message": "Budget created successfully."}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error creating budget: {str(e)}"}


def delete_budget(budget: Budget) -> dict:
    """Request to delete a budget.

    :param budget: Budget to delete.
    :type budget: Budget
    :return: Response object.
    :rtype: dict
    """
    try:
        db.delete(budget)
        db.commit()
        return {"success": True, "message": f"Budget deleted successfully."}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error deleting budget: {str(e)}"}


def add_funds(budget: Budget, amount: Decimal) -> dict:
    """Request to add funds to a budget.

    :param budget: Budget to modify.
    :type budget: Budget
    :param amount: Amount to add.
    :type amount: Decimal
    :return: Response object.
    :rtype: dict
    """
    try:
        budget.balance += amount
        db.commit()
        return {
            "success": True,
            "message": "Funds added succesfully.",
            "updatedBalance": budget.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error adding funds: {str(e)}"}


def remove_funds(budget: Budget, amount: Decimal) -> dict:
    """Request to remove funds from a budget.

    :param budget: Budget to modify.
    :type budget: Budget
    :param amount: Amount to remove.
    :type amount: Decimal
    :return: Response object.
    :rtype: dict
    """
    try:
        budget.balance -= amount
        db.commit()
        return {
            "success": True,
            "message": "Funds removed succesfully.",
            "updatedBalance": budget.balance,
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": f"Error removing funds: {str(e)}"}


def _get_budgets(user_email: str) -> list[Budget]:
    """Gets all of a user's budgets.

    :param email: User email.
    :type email: str
    :return: The user's budgets.
    :rtype: list[Budget]
    """
    return get_user(user_email).budgets


def get_budgets(user_email: str) -> dict:
    """Request to get all of a user's budgets.

    :param email: User email.
    :type email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        budgets = _get_budgets(user_email)
        return {
            "success": True,
            "message": "Budgets retrieved succesfully.",
            "budgets": budgets,
        }
    except Exception as e:
        return {"success": False, "error": f"Error retreiving budgets: {str(e)}"}


def _get_total_budgeted_funds(user_email: str) -> Decimal:
    """Get a user's total budgeted funds.

    :param email: User email.
    :type email: str
    :return: The user's total budgeted funds.
    :rtype: Decimal
    """
    # Get the user's budgets
    budgets: list[Budget] = _get_budgets(user_email)

    # Calculate the total amount of all budgets
    total = Decimal(0)
    for budget in budgets:
        total += budget.balance

    # Return the total
    return total


def get_total_budgeted_funds(user_email: str) -> dict:
    """Request to get a user's total budgeted funds.

    :param email: User email.
    :type email: str
    :return: Response object.
    :rtype: dict
    """
    try:
        total = _get_total_budgeted_funds(user_email)
        return {
            "success": True,
            "message": "Total budgeted funds retrieved successfully.",
            "total": total,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retreiving total budgeted funds: {str(e)}",
        }

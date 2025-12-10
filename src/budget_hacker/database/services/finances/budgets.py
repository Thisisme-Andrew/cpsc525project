"""Database services for budgets."""

from decimal import Decimal

from ....database.services.finances.constants import MAX_BALANCE
from ..users.users import _get_user
from ...models.models import Budget
from .... import db


def _create_budget(user_email: str, name: str, goal: Decimal):
    """Create and add a budget.

    :param user_email: User email.
    :type user_email: str
    :param name: Budget name.
    :type name: str
    :param goal: Budget goal.
    :type goal: Decimal
    """
    try:
        if goal > MAX_BALANCE:
            raise RuntimeError(
                f"Goal ${goal} exceeds the maximum allowed goal of ${MAX_BALANCE}."
            )
        budget = Budget(user_email=user_email, name=name, goal=goal, balance=Decimal(0))
        db.add(budget)
        db.commit()
    except Exception:
        db.rollback()
        raise


def create_budget(user_email: str, name: str, goal: Decimal) -> dict:
    """Request to create and add a budget.

    :param user_email: User email.
    :type user_email: str
    :param name: Budget name.
    :type name: str
    :param goal: Budget goal.
    :type goal: Decimal
    :return: Response object.
    :rtype: dict
    """
    try:
        _create_budget(user_email, name, goal)
        return {"success": True, "message": "Budget created successfully."}
    except Exception as e:
        return {"success": False, "error": f"Error creating budget: {str(e)}"}


def _delete_budget(budget: Budget):
    """Delete a budget.

    :param budget: Budget to delete.
    :type budget: Budget
    """
    try:
        db.delete(budget)
        db.commit()
    except Exception:
        db.rollback()
        raise ()


def delete_budget(budget: Budget) -> dict:
    """Request to delete a budget.

    :param budget: Budget to delete.
    :type budget: Budget
    :return: Response object.
    :rtype: dict
    """
    try:
        _delete_budget(budget)
        return {"success": True, "message": f"Budget deleted successfully."}
    except Exception as e:
        return {"success": False, "error": f"Error deleting budget: {str(e)}"}


def _add_funds(budget: Budget, amount: Decimal):
    """Add funds to a budget.

    :param budget: Budget to modify.
    :type budget: Budget
    :param amount: Amount to add.
    :type amount: Decimal
    """
    try:
        if budget.balance + amount > MAX_BALANCE:
            raise RuntimeError(
                f"Amount ${amount} plus current balance ${budget.balance} exceeds the maximum allowed budget balance of ${MAX_BALANCE}."
            )
        budget.balance += amount
        db.commit()
    except Exception:
        db.rollback()
        raise


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
        _add_funds(budget, amount)
        return {
            "success": True,
            "message": "Funds added succesfully.",
            "updatedBalance": budget.balance,
        }
    except Exception as e:
        return {"success": False, "error": f"Error adding funds: {str(e)}"}


def _remove_funds(budget: Budget, amount: Decimal):
    """Remove funds from a budget.

    :param budget: Budget to modify.
    :type budget: Budget
    :param amount: Amount to remove.
    :type amount: Decimal
    """
    try:
        if budget.balance - amount < 0:
            raise RuntimeError("Insufficient budget funds.")
        budget.balance -= amount
        db.commit()
    except Exception:
        db.rollback()
        raise


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
        _remove_funds(budget, amount)
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

    :param user_email: User email.
    :type user_email: str
    :return: The user's budgets.
    :rtype: list[Budget]
    """
    return _get_user(user_email).budgets


def get_budgets(user_email: str) -> dict:
    """Request to get all of a user's budgets.

    :param user_email: User email.
    :type user_email: str
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

    :param user_email: User email.
    :type user_email: str
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

    :param user_email: User email.
    :type user_email: str
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

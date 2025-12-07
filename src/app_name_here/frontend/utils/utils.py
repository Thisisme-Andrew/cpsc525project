"""
General utility functions.
"""

from collections import OrderedDict
from decimal import Decimal
import os
from textwrap import dedent
from typing import Any

from app_name_here.database.services.finances.accounts import get_account_balance
from app_name_here.database.services.finances.budgets import get_total_budgeted_funds
from .. import state


def get_choice_from_options(options: OrderedDict, prompt="Choose an option:") -> Any:
    """Displays and gets a chosen value from the provided options.

    :param options: Ordered dictionary of the available option names and their values.
    :type options: OrderedDict
    :return: The value of the chosen option.
    :rtype: typing.Any
    """
    while True:
        # Print the options prompt
        if prompt:
            print(prompt)

        # Parse and display the options in a numbered form.
        for i, name in enumerate(options.keys()):
            print(f"  {i}) {name}")

        # User input to choose an option by its number.
        choice = input("\nChoice: ")

        try:
            # Parse the chosen number
            choice_num = int(choice)
            if choice_num < 0:
                print("Choice must be a positive number! Please try again.\n")
                continue

            # Parse the option value for the chosen number
            chosen_value = list(options.values())[choice_num]
            print()
            return chosen_value

        except ValueError:
            print("Choice must be a number! Please try again.\n")
        except IndexError:
            print("Invalid choice! Please try again.\n")


def clear_screen():
    """Clears the app's screen."""
    # Citation: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    os.system("cls" if os.name == "nt" else "clear")


def str_to_decimal(str_num: str) -> Decimal | bool:
    """Converts a string to a decimal number with exactly 2 decimal places. Returns false if the
    conversion fails.

    :param str_num: Number to convert.
    :type str_num: str
    :return: The number as a Decimal with exactly 2 decimal places, or False if the conversion failed.
    :rtype: Decimal | bool
    """
    # Try an initial Decimal conversion
    try:
        val = Decimal(str_num)
    except:
        return False

    # Check for a decimal point
    parts = str_num.split(".")
    if len(parts) == 2:
        # Check for too many numbers after the decimal point
        decimals = len(parts[1])
        if decimals > 2:
            return False
    elif len(parts) > 2:
        # Invalid input (multiple decimal points)
        return False

    # Convert to Decimal with exactly 2 decimal places
    return val.quantize(Decimal("0.01"))


def get_account_and_budget_funds_report() -> str:
    """Gets a report of the user's finance account total, budgeted funds, and available funds.

    :return: Finance account and budget report.
    :rtype: str
    """
    # Get the user's account balance.
    balance_resp = get_account_balance(state.email)
    if not balance_resp["success"]:
        return "Failed to load the account balance."
    balance = balance_resp["balance"]

    # Get the user's total amount of budgeted funds
    total_budgeted_funds_resp = get_total_budgeted_funds(state.email)
    if not total_budgeted_funds_resp["success"]:
        return "Failed to load the total budgeted funds."
    total_budgeted_funds = total_budgeted_funds_resp["total"]

    return dedent(
        f"""\
            Account total: ${balance}
            Budgeted funds: ${total_budgeted_funds}
            Available funds: ${balance - total_budgeted_funds}"""
    )

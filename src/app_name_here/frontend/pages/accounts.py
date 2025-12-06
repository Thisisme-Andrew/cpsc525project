from time import sleep

from .page_templates import Page
from .. import state
from ..utils.utils import clear_screen
from decimal import Decimal
from ...database.services.finances.accounts import (
    get_account_balance,
    get_account_transactions,
    add_income,
    add_expense,
)


# for private use
def is_valid_number(string_input):
    try:
        val = Decimal(string_input)
    except:
        return False

    # Check decimal places
    parts = string_input.split(".")

    if len(parts) == 1:
        # integer → treat as 0 decimals
        decimals = 0
    elif len(parts) == 2:
        decimals = len(parts[1])
        if decimals > 2:
            return False
    else:
        # invalid string (multiple dots)
        return False

    # Convert to Decimal with exactly 2 decimal places
    val = val.quantize(Decimal("0.01"))
    return val


class GetBalancePage(Page):
    """Get Balance page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import FinanceDashboardPage

        clear_screen()
        # print(f"email is: {state.email}")
        while True:
            db_response = get_account_balance(state.email)
            if not db_response["success"]:
                print(f"Error: {db_response['error']}")
                user_response = input(
                    "Would you like to try again? (yes or any other key for no)"
                )
                if not user_response == "yes":
                    break
            else:
                print(f"Current balance: {db_response['balance']}")
                user_response = input(
                    "Enter any key to return to the finance Dashbaord"
                )
                break

        print("\nReturning to Finance Dashboard. Redirecting...")
        sleep(1)
        return FinanceDashboardPage()


class AddIncomePage(Page):
    """Adding income page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import FinanceDashboardPage

        clear_screen()

        while True:
            print("Please enter income amount or press Enter to go back:\n")

            income = input("Amount: ")
            if not income:
                break

            income = is_valid_number(income)
            if not income:
                print("Invalid Input!\n")
                continue
            elif income < 0:
                print("Amount must be positive!\n")
                continue
            else:
                print(
                    "Please enter a description or press Enter to cancel and go back:\n"
                )
                description = input("Description: ")
                if not description:
                    break
                else:
                    db_response = add_income(state.email, income, description)
                    if not db_response["success"]:
                        print(f"Error: {db_response['error']}")
                        user_response = input("Would you like to try again? (y or n): ")
                        if user_response in ["y", "yes"]:
                            clear_screen()
                            continue
                        else:
                            break
                    else:
                        print("Income added Successfully")
                        print(
                            f"Balance updated from {db_response['updatedBalance'] - income} to {db_response['updatedBalance']}"
                        )
                        user_response = input("Add another expense? (y or n): ")
                        if user_response not in ["y", "yes"]:
                            break
                        else:
                            clear_screen()

        print("\nReturning to Finance Dashboard. Redirecting...")
        sleep(1)
        return FinanceDashboardPage()


class AddExpensePage(Page):
    """Adding expense page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import FinanceDashboardPage

        clear_screen()

        while True:
            print("Please enter expense amount or press Enter to go back:\n")

            expense = input("Amount: ")
            if not expense:
                break

            expense = is_valid_number(expense)
            if not expense:
                print("Invalid Input!\n")
                continue
            elif expense < 0:
                print("Amount must be positive!\n")
                continue
            else:
                print(
                    "Please enter a description or press Enter to cancel and go back:\n"
                )
                description = input("Description: ")
                if not description:
                    break
                else:
                    db_response = add_expense(state.email, expense, description)
                    if not db_response["success"]:
                        print(f"Error: {db_response['error']}")
                        user_response = input("Would you like to try again? (y or n): ")
                        if user_response in ["y", "yes"]:
                            clear_screen()
                            continue
                        else:
                            break
                    else:
                        print("Expense added Successfully")
                        print(
                            f"Balance updated from {db_response['updatedBalance'] + expense} to {db_response['updatedBalance']}"
                        )
                        user_response = input("Add another expense? (y or n): ")
                        if user_response not in ["y", "yes"]:
                            break
                        else:
                            clear_screen()

        print("\nReturning to Finance Dashboard. Redirecting...")
        sleep(1)
        return FinanceDashboardPage()


class GetTransactionsPage(Page):
    """Get transaction history page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import FinanceDashboardPage

        clear_screen()
        while True:
            db_response = get_account_transactions(state.email)
            if not db_response["success"]:
                print(f"Error: {db_response['error']}")
                user_response = input(
                    "Would you like to try again? (yes or any other key for no)"
                )
                if not user_response == "yes":
                    break
            else:
                clear_screen()
                print("Transaction history:")
                i = 1
                for transaction in db_response["transactions"]:
                    print(f"-- TRANSACTION {i}--")
                    print(f"Date: {transaction.date}")
                    print(f"Starting Balance: {transaction.starting_balance}")
                    print(f"Amount: {transaction.amount}")
                    print(f"Type: {transaction.transaction_type}")
                    print(f"Description: {transaction.description}")
                    print(f"Ending Balance: {transaction.ending_balance}\n")
                    i += 1

                user_response = input(
                    "Enter any key to return to the finance Dashbaord"
                )
                break

        print("\nReturning to Finance Dashboard. Redirecting...")
        sleep(1)
        return FinanceDashboardPage()

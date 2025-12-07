"""Finance account pages."""

from collections import OrderedDict
from textwrap import dedent
from time import sleep

from .page_templates import Page, NavigationPage
from .. import state
from ..utils.utils import clear_screen, str_to_decimal
from ...database.services.finances.accounts import (
    get_account_balance,
    get_account_transactions,
    add_income,
    add_expense,
    send_money,
)
from ...database.services.finances.budgets import get_total_budgeted_funds


class AddIncomePage(Page):
    """Add income page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()
        print("Add Income\n")

        while True:
            print("Please enter income amount or press Enter to go back:\n")

            income = input("Amount: ")
            if not income:
                break

            income = str_to_decimal(income)
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
                        user_response = input("Add more income? (y or n): ")
                        if user_response not in ["y", "yes"]:
                            break
                        else:
                            clear_screen()

        print("\nReturning to the Finance Account Dashboard...")
        sleep(1)
        return FinanceAccountDashboardPage()


class AddExpensePage(Page):
    """Add expense page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()
        print("Add Expense\n")

        while True:
            print("Please enter expense amount or press Enter to go back:\n")

            expense = input("Amount: ")
            if not expense:
                break

            expense = str_to_decimal(expense)
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

        print("\nReturning to the Finance Account Dashboard...")
        sleep(1)
        return FinanceAccountDashboardPage()


class SendMoneyPage(Page):
    """Send money page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()
        print("Send Money\n")

        db_balance_response = get_account_balance(state.email)
        available_funds = "Unavailable"
        if db_balance_response["success"]:
            available_funds = db_balance_response["balance"]

        print(f"Available funds: ${available_funds}\n")

        while True:
            print("Please enter recipient email or press Enter to go back:\n")
            recipient_email = input("Recipient email: ")
            if not recipient_email:
                break

            while True:
                print("Please enter amount to send:\n")
                amount_to_send = input("Amount to send: ")
                amount_to_send = str_to_decimal(amount_to_send)
                if not amount_to_send:
                    print("Invalid amount!\n")
                elif amount_to_send < 0:
                    print("Amount must be positive!\n")
                else:
                    break

            print("Please enter a description or press Enter to cancel and go back:\n")
            description = input("Description: ")
            confirm = input(
                f'Send ${amount_to_send} to {recipient_email} with description: {description if description else "None"}? (y or n): '
            )
            if confirm not in ["y", "yes"]:
                retry = input("Would you like to try again? (y or n): ")
                if not retry:
                    break
                else:
                    continue

            db_response = send_money(
                state.email, recipient_email, amount_to_send, description
            )
            if not db_response["success"]:
                print(f"Error: {db_response['error']}")
                user_response = input("Would you like to try again? (y or n): ")
                if not user_response == "yes":
                    break
            else:
                print(f"{amount_to_send} sent to {recipient_email} successfully.")
                user_response = input(
                    "Press Enter to return to the finance Dashbaord: "
                )
                break

        print("\nReturning to the Finance Account Dashboard...")
        sleep(1)
        return FinanceAccountDashboardPage()


class AccountHistoryPage(Page):
    """Account history page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()
        print("Account History\n")

        while True:
            db_response = get_account_transactions(state.email)
            if not db_response["success"]:
                print(f"Error: {db_response['error']}")
                user_response = input("Would you like to try again? (y or n): ")
                if not user_response == "yes":
                    break
                continue
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

        print("\nReturning to the Finance Account Dashboard...")
        sleep(1)
        return FinanceAccountDashboardPage()


class FinanceAccountDashboardPage(NavigationPage):
    """Finance account dashboard page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import MainDashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Add Income", AddIncomePage),
                    ("Add Expense", AddExpensePage),
                    ("Send Money", SendMoneyPage),
                    ("Account History", AccountHistoryPage),
                    ("Go Back", MainDashboardPage),
                ]
            ),
            title="Finance Account Dashboard",
            clear_screen=True,
            subtitle="\n" + self.get_subtitle(),
        )

    @staticmethod
    def get_subtitle() -> str:
        """Gets the page's subtitle.

        :return: Page subtitle.
        :rtype: str
        """
        # Get the user's account balance.
        balance_resp = get_account_balance(state.email)
        if not balance_resp["success"]:
            return "Failed to load balance."
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

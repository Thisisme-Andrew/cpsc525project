"""Finance account pages."""

from collections import OrderedDict
from email_validator import validate_email, EmailNotValidError
from time import sleep

from .page_templates import Page, NavigationPage
from .. import state
from ..utils.utils import (
    clear_screen,
    get_account_and_budget_funds_report,
    str_to_decimal,
)
from ...database.services.finances.accounts import (
    get_transactions,
    add_income,
    add_expense,
    send_money,
)


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
            subtitle="\n" + get_account_and_budget_funds_report(),
        )


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
            print(
                "\nPlease enter a description or press Enter to cancel and go back:\n"
            )
            description = input("Description: ")
            if not description:
                break
            else:
                db_response = add_income(state.email, income, description)
                if not db_response["success"]:
                    print(db_response["error"] + "\n")
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
            print(
                "\nPlease enter a description or press Enter to cancel and go back:\n"
            )
            description = input("Description: ")
            if not description:
                break
            else:
                db_response = add_expense(state.email, expense, description)
                if not db_response["success"]:
                    print(db_response["error"] + "\n")
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

        # Display the user's account funds
        print(get_account_and_budget_funds_report() + "\n")

        while True:
            print("Please enter recipient email or press Enter to go back:\n")
            recipient_email = input("Recipient email: ")
            if not recipient_email:
                break
            try:
                validate_email(recipient_email)
            except EmailNotValidError:
                print("Invalid email format. Please try again.\n")
                continue
            print()

            while True:
                print("Please enter an amount to send or press Enter to go back:\n")
                amount_to_send = input("Amount to send: ")
                if not amount_to_send:
                    break
                amount_to_send = str_to_decimal(amount_to_send)
                if not amount_to_send:
                    print("Invalid amount!\n")
                    continue
                elif amount_to_send < 0:
                    print("Amount must be positive!\n")
                print()
                break

            print("Please enter a description:\n")
            description = input("Description: ")
            print()
            confirm = input(
                f'Send ${amount_to_send} to {recipient_email} with description: {description if description else "None"}? (y or n): '
            )
            if confirm not in ["y", "yes"]:
                retry = input("Would you like to try again? (y or n): ")
                print()
                if retry not in ["y", "yes"]:
                    break
                continue
            print()

            db_response = send_money(
                state.email, recipient_email, amount_to_send, description
            )
            if not db_response["success"]:
                print(db_response["error"] + "\n")
                retry = input("Would you like to try again? (y or n): ")
                print()
                if retry not in ["y", "yes"]:
                    break
                continue

            print(f"{amount_to_send} sent to {recipient_email} successfully.\n")
            input("Press Enter to return to the previous page...")
            return FinanceAccountDashboardPage()

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
            db_response = get_transactions(state.email)
            if not db_response["success"]:
                print(db_response["error"] + "\n")
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

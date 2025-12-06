from collections import OrderedDict
from textwrap import dedent
from time import sleep

from app_name_here.frontend.pages.dashboard import FinanceDashboardPage

from .users import LoginPage, CreateAccountPage, LogoutPage
from .page_templates import NavigationPage, Page
from .settings import SettingsPage
from .. import state
from .accounts import (
    AddIncomePage,
    AddExpensePage,
    GetTransactionsPage,
    is_valid_number,
)
from ...database.services.finances.accounts import get_account_balance
from ...database.services.finances.budgets import (
    add_funds,
    get_budgets,
    get_total_budgeted_funds,
)
from ..utils.utils import clear_screen, get_choice_from_options
from prettytable import PrettyTable
from ...database.models.models import Budget


def budgets_to_table(budgets: list[Budget]) -> str:
    """Creates a table for displaying budgets.

    :param budgets: Budgets to display.
    :type budgets: list[Budget]
    :return: The string representation of a budgets table.
    :rtype: str
    """
    # Print a message if the list of budgets is empty
    if not budgets:
        print("No active budgets.")
        return

    # Create a table to display the budgets
    table = PrettyTable()
    table.field_names = [
        "Name",
        "Current Balance ($)",
        "Goal ($)",
    ]
    for budget in budgets:
        table.add_row([budget.name, budget.balance, budget.goal])

    # Return the table's string representation
    return table.get_string()


def display_all_budgets():
    # Get the user's budgets
    budgets_resp = get_budgets(state.email)
    if not budgets_resp["success"]:
        raise RuntimeError(budgets_resp["error"])
    budgets = budgets_resp["budgets"]

    # Return a table for the budgets
    return budgets_to_table(budgets)


class BudgetsDashboardPage(NavigationPage):
    """Budgets dashboard page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .dashboard import FinanceDashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Manage Budgets", ManageBudgetsPage),
                    ("Create a Budget", None),
                    ("Go Back", FinanceDashboardPage),
                ]
            ),
            title="Budgets Dashboard",
            clear_screen=True,
            subtitle="\n" + display_all_budgets(),
        )


class ManageBudgetsPage(Page):
    """Manage budgets page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Clear the screen.
        clear_screen()

        # Display the page title
        print("Manage Budgets\n")

        # Get the user's budgets
        budgets_resp = get_budgets(state.email)
        if not budgets_resp["success"]:
            raise RuntimeError(budgets_resp["error"])
        budgets = budgets_resp["budgets"]

        # Display a table for the budgets
        print(budgets_to_table(budgets) + "\n")

        # Handle if the user has no budgets
        if not budgets:
            input("Press Enter to go back...")
            print("\nReturning to Budget Dashboard...")
            sleep(1)
            return BudgetsDashboardPage

        # Choose a budget to manage
        budget_options = OrderedDict([(budget.name, budget) for budget in budgets])
        budget_options["Go Back"] = BudgetsDashboardPage
        chosen_budget: Budget | BudgetsDashboardPage = get_choice_from_options(
            budget_options, prompt="Choose a budget:"
        )

        # Handle the "Go Back" option
        if chosen_budget is BudgetsDashboardPage:
            return chosen_budget()

        return ManageBudgetPage(chosen_budget)


class ManageBudgetPage(NavigationPage):
    """Manage budget page."""

    def __init__(self, budget: Budget):
        """Constructs the page for the provided budget.

        :param budget: Budget to use.
        :type budget: Budget
        """
        super().__init__(
            options=OrderedDict(
                [
                    ("Add Funds", AddFundsPage(budget)),
                    ("Remove Funds", None),
                    ("Delete Budget", None),
                    ("Go Back", ManageBudgetsPage),
                ]
            ),
            title="Manage Budget",
            clear_screen=True,
            subtitle="\n" + budgets_to_table([budget]),
        )


class AddFundsPage(Page):
    """Page to add funds to a budget."""

    def __init__(self, budget: Budget):
        """Constructs the page for the provided budget.

        :param budget: Budget to use.
        :type budget: Budget
        """
        self.budget = budget

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()

        # Display a table for the budget
        print(budgets_to_table([self.budget]) + "\n")

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

        available_account_funds = balance - total_budgeted_funds

        # Display the user's account funds
        print(FinanceDashboardPage.get_subtitle() + "\n")

        while True:
            # Get the amount of funds to add
            print("Please enter an amount of funds to add or press Enter to go back:\n")
            funds = input("Amount: ")
            if not funds:
                break

            # Amount validation
            funds = is_valid_number(funds)
            if not funds:
                print("Invalid Input!\n")
                continue
            if funds < 0:
                print("Amount must be positive!\n")
                continue
            if funds > available_account_funds:
                print("Amount must not exceed your available account funds!\n")
                continue

            # Request to add funds
            add_funds_resp = add_funds(self.budget, funds)
            if not add_funds_resp["success"]:
                print(add_funds_resp["error"])
                break
            print(add_funds_resp["message"])

            # Goal reached message
            if self.budget.balance >= self.budget.goal:
                print("\nCongratulations, you fulfilled your budget goal!\n")
                input("Press Enter to continue...")

            break

        print("\nReturning to the previous page...")
        sleep(1.5)
        return ManageBudgetPage(self.budget)

from collections import OrderedDict
from textwrap import dedent
from time import sleep

from .users import LoginPage, CreateAccountPage, LogoutPage
from .page_templates import NavigationPage, Page
from .settings import SettingsPage
from .. import state
from .accounts import AddIncomePage, AddExpensePage, GetTransactionsPage
from ...database.services.finances.accounts import get_account_balance
from ...database.services.finances.budgets import get_budgets, get_total_budgeted_funds
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
        chosen_budget: Budget = get_choice_from_options(
            budget_options, prompt="Choose a budget:"
        )
        print(f"You chose: {chosen_budget.name}")


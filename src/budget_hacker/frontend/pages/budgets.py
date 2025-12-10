"""Budget pages."""

from collections import OrderedDict
from prettytable import PrettyTable
from time import sleep

from .page_templates import NavigationPage, Page
from .. import state
from ..utils.utils import (
    clear_screen,
    get_account_and_budget_funds_report,
    get_choice_from_options,
    str_to_decimal,
)
from ...database.models.models import Budget
from ...database.services.finances.accounts import (
    get_available_account_funds,
)
from ...database.services.finances.budgets import (
    add_funds,
    create_budget,
    delete_budget,
    get_budgets,
    remove_funds,
)


def budgets_to_table(budgets: list[Budget]) -> str:
    """Creates a table for displaying budgets.

    :param budgets: Budgets to display.
    :type budgets: list[Budget]
    :return: The string representation of a budgets table.
    :rtype: str
    """
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


def display_all_budgets() -> str:
    """Displays a table for all of the user's budgets.

    :raises RuntimeError: If the user's budgets can't be retrieved.
    :return: The string representation of a budgets table.
    :rtype: str
    """
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
        from .main_dashboard import MainDashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Edit Budgets", ManageBudgetsPage),
                    ("Create a Budget", CreateBudgetPage),
                    ("Go Back", MainDashboardPage),
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
        print("--Manage Budgets--\n")

        # Get the user's budgets
        budgets_resp = get_budgets(state.email)
        if not budgets_resp["success"]:
            raise RuntimeError(budgets_resp["error"])
        budgets = budgets_resp["budgets"]

        # Display a table for the budgets
        print(budgets_to_table(budgets) + "\n")

        # Handle if the user has no budgets
        if not budgets:
            input("No budgets available. Press Enter to go back...")
            print("\nReturning to the Budget Dashboard...")
            sleep(1)
            return BudgetsDashboardPage()

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
                    ("Remove Funds", RemoveFundsPage(budget)),
                    ("Delete Budget", DeleteBudgetPage(budget)),
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
        print("--Add Funds--\n")

        # Display a table for the budget
        print(budgets_to_table([self.budget]) + "\n")

        # Get the user's available account funds
        available_account_funds_resp = get_available_account_funds(state.email)
        if not available_account_funds_resp["success"]:
            print(available_account_funds_resp["error"] + "\n")
            input("Press Enter to return to the previous page...")
            return ManageBudgetPage(self.budget)
        available_account_funds = available_account_funds_resp["availableFunds"]

        # Display the user's account funds
        print(get_account_and_budget_funds_report() + "\n")

        while True:
            # Get the amount of funds to add
            print("Please enter an amount of funds to add or press Enter to go back:\n")
            amount = input("Amount: ")
            if not amount:
                break

            # Amount validation
            amount = str_to_decimal(amount)
            if not amount:
                print("Invalid Input!\n")
                continue
            if amount < 0:
                print("Amount must be positive!\n")
                continue
            if amount > available_account_funds:
                print("Amount must not exceed your available account funds!\n")
                continue
            print()

            # Request to add funds
            add_funds_resp = add_funds(self.budget, amount)
            if not add_funds_resp["success"]:
                print(add_funds_resp["error"] + "\n")
                input("Press Enter to return to the previous page...")
                return ManageBudgetPage(self.budget)
            print(add_funds_resp["message"])

            # Goal reached message
            if self.budget.balance >= self.budget.goal:
                print("\nCongratulations, you fulfilled your budget goal!\n")
                input("Press Enter to continue...")

            break

        print("\nReturning to the previous page...")
        sleep(1.5)
        return ManageBudgetPage(self.budget)


class RemoveFundsPage(Page):
    """Page to remove funds from a budget."""

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
        print("--Remove Funds--\n")

        # Display a table for the budget
        print(budgets_to_table([self.budget]) + "\n")

        # Display the user's account funds
        print(get_account_and_budget_funds_report() + "\n")

        while True:
            # Get the amount of funds to remove
            print(
                "Please enter an amount of funds to remove or press Enter to go back:\n"
            )
            amount = input("Amount: ")
            if not amount:
                break

            # Amount validation
            amount = str_to_decimal(amount)
            if not amount:
                print("Invalid Input!\n")
                continue
            if amount < 0:
                print("Amount must be positive!\n")
                continue
            if amount > self.budget.balance:
                print("Amount must not exceed the budget's current balance!\n")
                continue
            print()

            # Request to remove funds
            remove_funds_resp = remove_funds(self.budget, amount)
            if not remove_funds_resp["success"]:
                print(remove_funds_resp["error"] + "\n")
                continue
            print(remove_funds_resp["message"])
            break

        print("\nReturning to the previous page...")
        sleep(1.5)
        return ManageBudgetPage(self.budget)


class DeleteBudgetPage(Page):
    """Delete budget page."""

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
        print("--Delete Budget--\n")

        while True:
            # Display a table for the budget
            print(budgets_to_table([self.budget]) + "\n")

            confirm = input("Are you sure you want to delte this budget? (y or n): ")
            if not confirm.lower() in ["y", "yes"]:
                print("Aborting...")
                sleep(1)
                return ManageBudgetPage(self.budget)

            # Request to delete budget
            delete_budget_resp = delete_budget(self.budget)
            if not delete_budget_resp["success"]:
                print(delete_budget_resp["error"] + "\n")
                continue
            print(delete_budget_resp["message"])
            break

        print("\nReturning to the previous page...")
        sleep(1.5)
        return BudgetsDashboardPage()


class CreateBudgetPage(Page):
    """Create budget page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clear_screen()
        print("--Create Budget--\n")

        print("Create a budget or press Enter to go back:\n")

        while True:
            # Get the budget name
            name = input("Budget name: ")
            if not name:
                print("Returning to the previous page...")
                return BudgetsDashboardPage()

            # Validate the name
            if len(name) < 3:
                print("Name must be at least 3 characters. Please try again.\n")
                continue
            if name.lower() == "go back":
                print("Invalid name. Please try again.\n")
            break

        while True:
            # Get the budget goal amount
            goal = input("Budget goal ($): ")
            if not goal:
                print("Returning to the previous page...")
                return BudgetsDashboardPage()

            # Validate the goal
            goal = str_to_decimal(goal)
            if not goal:
                print("Invalid Input! Please try again.\n")
                continue
            if goal < 0:
                print("Goal must be positive! Please try again.\n")
                continue

            # Request to create the budget
            create_budget_resp = create_budget(state.email, name, goal)
            if not create_budget_resp["success"]:
                print(create_budget_resp["error"] + "\n")
                retry = input("Would you like to try again? (y or n): ")
                if retry in ["y", "yes"]:
                    return CreateBudgetPage()
                break
            print(create_budget_resp["message"])
            break

        print("\nReturning to the previous page...")
        sleep(1.5)
        return BudgetsDashboardPage()

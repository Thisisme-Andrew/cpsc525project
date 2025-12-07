from collections import OrderedDict
from textwrap import dedent

from .users import LoginPage, CreateUserPage, LogoutPage
from .page_templates import NavigationPage
from .settings import SettingsPage
from .. import state
from .accounts import AddIncomePage, AddExpensePage, GetTransactionsPage, SendMoneyPage
from ...database.services.finances.accounts import get_account_balance
from ...database.services.finances.budgets import get_total_budgeted_funds


class WelcomePage(NavigationPage):
    """Welcome page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Log In", LoginPage),
                    ("Create an Account", CreateUserPage),
                    ("Exit", None),
                ]
            ),
            title="Welcome to <TODO-App-Name>!",
            clear_screen=True,
        )


class DashboardPage(NavigationPage):
    """Dashboard page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Finance Dashboard", FinanceDashboardPage),
                    ("Settings", SettingsPage),
                    ("Log Out", LogoutPage),
                    ("Exit", None),
                ]
            ),
            title="<TODO-App-Name> Dashboard",
            clear_screen=True,
        )


class FinanceDashboardPage(NavigationPage):
    """Finances page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .dashboard import DashboardPage
        from .budgets import BudgetsDashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Add Income", AddIncomePage),
                    ("Add Expense", AddExpensePage),
                    ("Send Money", SendMoneyPage),
                    ("Budgets Dashboard", BudgetsDashboardPage),
                    ("See Account History", GetTransactionsPage),
                    ("Go Back", DashboardPage),
                ]
            ),
            title="Finance Dashboard",
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

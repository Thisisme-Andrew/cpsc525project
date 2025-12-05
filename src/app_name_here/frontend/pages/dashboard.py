from collections import OrderedDict
from textwrap import dedent

from .account import LoginPage, CreateAccountPage, LogoutPage
from .page_templates import NavigationPage
from .settings import SettingsPage
from .. import state
from .finances import AddIncomePage, AddExpensePage, GetTransactionsPage
from ...database.services.finances.finance_services import get_account_balance


class WelcomePage(NavigationPage):
    """Welcome page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Log In", LoginPage),
                    ("Create an Account", CreateAccountPage),
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

        super().__init__(
            options=OrderedDict(
                [
                    ("Add Income", AddIncomePage),
                    ("Add Expense", AddExpensePage),
                    ("See Account History", GetTransactionsPage),
                    ("Go Back", DashboardPage),
                ]
            ),
            title="Finance Dashboard",
            clear_screen=True,
            sub_title="\n" + self.get_subtitle(),
            # sub_title=(
            #     f"balance: {get_balance(state.email)['balance']}"
            #     if get_balance(state.email)["success"]
            #     else "Error"
            # ),
        )

    @staticmethod
    def get_subtitle():
        balance_response = get_account_balance(state.email)
        if not balance_response["success"]:
            return "Failed to load balance."

        balance = balance_response["balance"]

        msg = f"""Account total: {balance}
            Available funds: {balance} TODO
            Budgeted funds: {balance} TODO"""

        return dedent(msg)

from collections import OrderedDict

from .account import LoginPage, CreateAccountPage, LogoutPage
from .page_templates import NavigationPage
from .settings import SettingsPage
from .. import state
from .finances import AddIncome, AddExpense, GetTransactions
from ...database.services.finances.finance_services import get_balance


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
                    ("Add Income", AddIncome),
                    ("Add Expense", AddExpense),
                    ("See Account History", GetTransactions),
                    ("Go Back", DashboardPage),
                ]
            ),
            title="Finances",
            clear_screen=True,
            sub_title=f"balance: {get_balance(state.email)['balance']}" if get_balance(state.email)['success'] else "Error"
        )

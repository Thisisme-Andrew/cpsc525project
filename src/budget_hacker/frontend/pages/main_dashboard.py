"Main dashboard pages."

from collections import OrderedDict

from .page_templates import NavigationPage
from .settings import SettingsPage
from .users import LoginPage, CreateUserPage, LogoutPage
from ..utils.utils import get_account_and_budget_funds_report


class WelcomePage(NavigationPage):
    """Welcome page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Log In", LoginPage),
                    ("Create a User Account", CreateUserPage),
                    ("Exit", None),
                ]
            ),
            title="Welcome to Budget Hacker!",
            subtitle="\nTake greater control over your finances with a personal budget tracker!",
            clear_screen=True,
        )


class MainDashboardPage(NavigationPage):
    """Main dashboard page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .budgets import BudgetsDashboardPage
        from .accounts import AddIncomePage, AddExpensePage, SendMoneyPage, AccountHistoryPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Add Income", AddIncomePage),
                    ("Add Expense", AddExpensePage),
                    ("Send Money", SendMoneyPage),
                    ("Account History", AccountHistoryPage),
                    ("Manage Budgets", BudgetsDashboardPage),
                    ("Settings", SettingsPage),
                    ("Log Out", LogoutPage),
                    ("Exit", None),
                ]
            ),
            title="Budget Hacker Dashboard",
            clear_screen=True,
            subtitle="\n" + get_account_and_budget_funds_report()
        )

from collections import OrderedDict

from .account import ChangePasswordPage, DeleteAccountPage
from .page_templates import NavigationPage


class SettingsPage(NavigationPage):
    """Settings page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .dashboard import DashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Change Password", ChangePasswordPage),
                    ("Delete Account", DeleteAccountPage),
                    ("Go Back", DashboardPage),
                ]
            ),
            title="Settings",
            clear_screen=True,
        )

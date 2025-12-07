from collections import OrderedDict

from .users import ChangePasswordPage, DeleteUserPage
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
                    ("Delete Account", DeleteUserPage),
                    ("Go Back", DashboardPage),
                ]
            ),
            title="Settings",
            clear_screen=True,
        )

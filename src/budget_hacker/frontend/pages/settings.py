"""Settings pages."""

from collections import OrderedDict

from .page_templates import NavigationPage
from .users import ChangePasswordPage, DeleteUserPage


class SettingsPage(NavigationPage):
    """Settings page."""

    def __init__(self):
        """Constructs the page."""
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import MainDashboardPage

        super().__init__(
            options=OrderedDict(
                [
                    ("Change Password", ChangePasswordPage),
                    ("Delete Account", DeleteUserPage),
                    ("Go Back", MainDashboardPage),
                ]
            ),
            title="Settings",
            clear_screen=True,
        )

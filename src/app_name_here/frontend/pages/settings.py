from collections import OrderedDict

from .account import ChangePasswordPage
from .page_templates import NavigationPage


class SettingsPage(NavigationPage):
    """Settings page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Change Password", ChangePasswordPage()),
                    ("Delete Account", None),
                ]
            ),
            title="Settings",
            clear_screen=True,
        )

from collections import OrderedDict

from .auth import LoginPage, CreateAccountPage
from .page_templates import NavigationPage


class DashboardPage(NavigationPage):
    """Dashboard page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("<TODO OPTION 0>", None),
                    ("<TODO OPTION 1>", None),
                    ("Settings", None),
                    ("Exit", None),
                ]
            ),
            title="<TODO-App-Name> Dashboard",
            clear_screen=True,
        )


class WelcomePage(NavigationPage):
    """Welcome page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Log In", LoginPage()),
                    ("Create an Account", CreateAccountPage()),
                    ("Exit", None),
                ]
            ),
            title="Welcome to <TODO-App-Name>!",
            clear_screen=True,
        )

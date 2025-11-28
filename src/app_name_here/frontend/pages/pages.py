"""
General application pages.
"""

from collections import OrderedDict
import sys

from .base_pages import Page, NavigationPage
from ..utils.utils import clearScreen


class WelcomePage(NavigationPage):
    """Welcome page."""

    def __init__(self):
        """Constructs the page."""
        super().__init__(
            options=OrderedDict(
                [
                    ("Log In", LoginPage()),
                    ("Create an Account", LoginPage),
                    ("Exit", None),
                ]
            ),
            title="Welcome to <TODO-App-Name>!",
            clear_screen=True,
        )


class LoginPage(Page):
    """Login page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        clearScreen()
        print("Please enter your login credentals:\n")

        while True:
            # Get the user's credentials
            email = input("Email: ")
            if email in ["", "e"]:
                # Return to the welcome page
                print()
                return WelcomePage()

            password = input("Password: ")

            # TODO verify credentials
            if email != "" and password != "":
                return WelcomePage()

            print("Invalid credentials! Try again or press Enter to go back.\n")


class CreateAccountPage(Page):
    """Create account page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        print("On the dashboard page. Not implemented yet, exiting...")
        sys.exit(0)


class DashboardPage(Page):
    """Dashboard page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        print("On the dashboard page. Not implemented yet, exiting...")
        sys.exit(0)

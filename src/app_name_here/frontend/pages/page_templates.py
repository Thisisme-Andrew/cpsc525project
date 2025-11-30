"""
Application page base class and templates.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
import sys

from ..utils.utils import clear_screen, get_choice_from_options


class Page(ABC):
    """Base class for app pages."""

    @abstractmethod
    def run(self) -> "Page":
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        raise NotImplementedError()


class NavigationPage(Page, ABC):
    """Base class for pages used purely to navigate between other pages."""

    def __init__(self, options: OrderedDict, title: str, clear_screen: bool = False, sub_title: str = None):
        """Construct a navigation page from the provided parameters.

        :param options: The available page options.
        :type options: OrderedDict
        :param title: Title to display for the page.
        :type title: str
        :param clear_screen: Flag to enable clearning the app's screen before dispalying the page,
            defaults to False
        :type clear_screen: bool, optional
        """
        self.options = options
        self.title = title
        self.sub_title = sub_title
        self.clear_screen = clear_screen

    def run(self) -> Page:
        """Runs the page. Exits the app if a page is not chosen.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Clear the screen if desired.
        if self.clear_screen:
            clear_screen()

        # Display the page title if provided.
        if self.title is not None:
            print(f"{self.title}")
            if not self.sub_title:
                print()
        
        if self.sub_title is not None:
            print(f"{self.sub_title}\n")

        # Get the next page to navigate to.
        chosen_page = get_choice_from_options(self.options)

        # Exit the app if the chosen page is None.
        if chosen_page is None:
            print("Thank you for using <TODO-App-Name>! Goodbye.")
            sys.exit(0)

        # Return an instance of the chosen page
        return chosen_page()

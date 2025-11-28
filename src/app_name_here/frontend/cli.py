from .pages.base_pages import Page
from .pages.pages import WelcomePage


class CLI:
    """Main application CLI."""

    def __init__(self):
        """Initialize the CLI with a default page."""
        self.current_page: Page = WelcomePage()

    def run(self):
        """CLI run loop. Runs until a page makes a system exit call."""
        while True:
            # Each page returns the nxt page after it runs
            self.current_page = self.current_page.run()
